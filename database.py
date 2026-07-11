import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId 

# Load environment variables from .env file we use -> 
load_dotenv()

class MongoDBHandler:
    """Handles all MongoDB operations for MeetMind."""
    
    def __init__(self, connection_string=None, db_name="meetmind_db"):
        """
        Initializes the MongoDB connection.
        
        Args:
            connection_string: The Atlas connection string. If None, reads from .env.
            db_name: The name of the database (default: "meetmind_db").
        """
        # If connection_string is not provided, get it from environment variables
        if connection_string is None:
            connection_string = os.getenv("MONGO_URI")
            
        if not connection_string:
            raise ValueError(" No MongoDB connection string found! Set MONGO_URI in .env file.")
        
        self.connection_string = connection_string
        self.db_name = db_name
        self.client = None
        self.db = None
    
    def connect(self):
        """
        Establishes the connection to MongoDB Atlas.
        """
        try:
            self.client = MongoClient(self.connection_string)
            self.db = self.client[self.db_name]
            self.client.admin.command('ping')
            print(" Successfully connected to MongoDB Atlas!")
            return True
        except Exception as e:
            print(f" Failed to connect to MongoDB: {e}")
            return False
    
    def save_meeting(self, meeting_text, action_items, meeting_title="Untitled Meeting"):
        """
        Saves a meeting and its action items to the database.
        """
        if self.db is None:
            print(" Not connected to database. Call connect() first.")
            return None
        
        action_dicts = [item.to_dict() for item in action_items]
        
        meeting_document = {
            "meeting_title": meeting_title,
            "meeting_text": meeting_text,
            "action_items": action_dicts,
            "created_at": datetime.now(),
            "total_actions": len(action_items)
        }
        
        try:
            result = self.db.meetings.insert_one(meeting_document)
            print(f" Meeting '{meeting_title}' saved to MongoDB! (ID: {result.inserted_id})")
            return result.inserted_id
        except Exception as e:
            print(f" Failed to save meeting: {e}")
            return None
    
    def get_all_meetings(self):
        """
        Retrieves all meetings from the database.
        """
        if self.db is None:
            print(" Not connected to database.")
            return []
        
        try:
            meetings = list(self.db.meetings.find())
            print(f" Found {len(meetings)} meetings in database.")
            return meetings
        except Exception as e:
            print(f" Failed to retrieve meetings: {e}")
            return []
    
    def get_pending_actions(self, assignee=None):
        """
        Retrieves all pending action items.
        Optionally filter by assignee.
        """
        if self.db is None:
            print(" Not connected to database.")
            return []
        
        try:
            pipeline = [
                {"$unwind": "$action_items"},
                {"$match": {"action_items.is_completed": False}}
            ]
            
            if assignee:
                pipeline[1]["$match"]["action_items.assignee"] = assignee
            
            results = list(self.db.meetings.aggregate(pipeline))
            pending = [item["action_items"] for item in results]
            
            print(f" Found {len(pending)} pending action items.")
            return pending
            
        except Exception as e:
            print(f" Failed to get pending actions: {e}")
            return []
    


    def mark_action_complete(self, meeting_id, action_index):
        """
        Marks a specific action item as completed.
        
        Args:
            meeting_id: The ID of the meeting (as a string).
            action_index: The index of the action item in the list (0-based).
        
        Returns:
            True if successful, False otherwise.
        """
        if self.db is None:
            print(" Not connected to database.")
            return False
        
        try:
            obj_id = ObjectId(meeting_id)
            
            # Build the dynamic field name: action_items.0.is_completed
            update_field = f"action_items.{action_index}.is_completed"
            
            result = self.db.meetings.update_one(
                {"_id": obj_id},
                {"$set": {update_field: True}}
            )
            
            if result.modified_count > 0:
                print(f" Action item {action_index} marked as complete.")
                return True
            else:
                print(" No action item was updated. Check the ID and index.")
                return False
                
        except Exception as e:
            print(f" Failed to update action item: {e}")
            return False
    
    def close(self):
        """
        Closes the MongoDB connection.
        """
        if self.client:
            self.client.close()
            print(" MongoDB connection closed.")