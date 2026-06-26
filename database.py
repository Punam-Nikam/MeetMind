
import os
from dotenv import load_dotenv  # <-- NEW: For reading .env file
from pymongo import MongoClient
from datetime import datetime

# Load environment variables from .env file
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
            raise ValueError("❌ No MongoDB connection string found! Set MONGO_URI in .env file.")
        
        self.connection_string = connection_string
        self.db_name = db_name
        self.client = None
        self.db = None
    
    def connect(self):
        """
        Establishes the connection to MongoDB Atlas.
        """
        try:
            # Create a MongoDB client
            self.client = MongoClient(self.connection_string)
            
            # Select the database
            self.db = self.client[self.db_name]
            
            # Ping the database to test the connection
            self.client.admin.command('ping')
            
            print("✅ Successfully connected to MongoDB Atlas!")
            return True
            
        except Exception as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            return False
    
    def save_meeting(self, meeting_text, action_items):
        """
        Saves a meeting and its action items to the database.
        
        Args:
            meeting_text: The original meeting notes text.
            action_items: A list of ActionItem objects.
        
        Returns:
            The inserted document's ID.
        """
        # Check if we are connected
        if self.db is None:
            print("❌ Not connected to database. Call connect() first.")
            return None
        
        # Convert action items to dictionaries (using our to_dict() method)
        action_dicts = [item.to_dict() for item in action_items]
        
        # Create the meeting document
        meeting_document = {
            "meeting_text": meeting_text,
            "action_items": action_dicts,
            "created_at": datetime.now(),  # When this was saved
            "total_actions": len(action_items)
        }
        
        try:
            # Insert the document into the "meetings" collection
            result = self.db.meetings.insert_one(meeting_document)
            
            # Get the inserted ID
            inserted_id = result.inserted_id
            
            print(f"✅ Meeting saved to MongoDB! (ID: {inserted_id})")
            print(f"   📋 {len(action_items)} action items stored.")
            
            return inserted_id
            
        except Exception as e:
            print(f"❌ Failed to save meeting: {e}")
            return None
    
    def get_all_meetings(self):
        """
        Retrieves all meetings from the database.
        """
        if self.db is None:
            print("❌ Not connected to database.")
            return []
        
        try:
            meetings = list(self.db.meetings.find())
            print(f"📁 Found {len(meetings)} meetings in database.")
            return meetings
        except Exception as e:
            print(f"❌ Failed to retrieve meetings: {e}")
            return []
    
    def get_pending_actions(self, assignee=None):
        """
        Retrieves all pending action items.
        Optionally filter by assignee.
        """
        if self.db is None:
            print("❌ Not connected to database.")
            return []
        
        try:
            # Aggregation pipeline to "unwind" the action_items array
            pipeline = [
                {"$unwind": "$action_items"},
                {"$match": {"action_items.is_completed": False}}
            ]
            
            # If assignee is provided, add it to the filter
            if assignee:
                pipeline[1]["$match"]["action_items.assignee"] = assignee
            
            results = list(self.db.meetings.aggregate(pipeline))
            
            # Extract just the action items
            pending = [item["action_items"] for item in results]
            
            print(f"📋 Found {len(pending)} pending action items.")
            return pending
            
        except Exception as e:
            print(f"❌ Failed to get pending actions: {e}")
            return []
    
    def close(self):
        """
        Closes the MongoDB connection.
        """
        if self.client:
            self.client.close()
            print("🔒 MongoDB connection closed.")