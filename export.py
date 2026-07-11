# export.py

import csv
from database import MongoDBHandler

class CSVExporter:
    """
    This class handles exporting action items from MongoDB to CSV files.
    CSV files can be opened in Excel, Google Sheets, or any text editor.
    """
    
    def __init__(self, db_handler):
        """
        The constructor receives a database handler object.
        We store it so we can reuse it for multiple exports.
        """
        self.db_handler = db_handler
    
    def export_all_actions(self, filename="all_actions.csv"):
        """
        Exports EVERY action item from ALL meetings to a CSV file.
        This includes both completed and pending tasks.
        
        Args:
            filename: The name of the CSV file to create.
        
        Returns:
            True if successful, False if failed.
        """
        
        # --- Step 1: Connect to the database ---
        # If we can't connect, stop and return False
        if not self.db_handler.connect():
            print("Could not connect to database.")
            return False
        
        # --- Step 2: Fetch all meetings from MongoDB ---
        # get_all_meetings() returns a list of meeting documents
        meetings = self.db_handler.get_all_meetings()
        
        # If there are no meetings, nothing to export
        if not meetings:
            print(" No meetings found in database.")
            return False
        
        # --- Step 3: Prepare the data for CSV ---
        # We need to flatten the nested structure.
        # Each meeting has a list of action_items.
        # We want ONE row per action item.
        rows = []
        
        for meeting in meetings:
            # Convert the ObjectId to a string so it can be stored in CSV
            meeting_id = str(meeting['_id'])
            
            # Get the creation timestamp (if it exists)
            created_at = meeting.get('created_at', 'Unknown')
            
            # Loop through each action item inside this meeting
            for action in meeting.get('action_items', []):
                # Create a dictionary for ONE row in the CSV
                rows.append({
                    "Meeting ID": meeting_id,
                    "Created At": created_at,
                    "Description": action.get('description', ''),
                    "Assignee": action.get('assignee', 'Unassigned'),
                    "Due Date": action.get('due_date', 'Not specified'),
                    "Status": "Completed" if action.get('is_completed') else "Pending"
                })
        
        # --- Step 4: Write the data to a CSV file ---
        try:
            # 'with open' is a context manager. It automatically closes the file.
            # 'w' = write mode.
            # 'newline=""' prevents extra blank lines in the CSV on Windows.
            # 'encoding="utf-8"' supports all characters (like emojis or accents).
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                
                # Define the column headers in the exact order we want
                fieldnames = ["Meeting ID", "Created At", "Description", "Assignee", "Due Date", "Status"]
                
                # Create a CSV writer that uses dictionaries
                # This means we can just pass our dictionary and it matches the keys to columns
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                # Write the header row (the column names)
                writer.writeheader()
                
                # Write all the data rows (our list of dictionaries)
                writer.writerows(rows)
            
            print(f"Successfully exported {len(rows)} action items to '{filename}'")
            return True
            
        except Exception as e:
            # If anything goes wrong (e.g., permission denied), catch it here
            print(f"Failed to export CSV: {e}")
            return False
        
        finally:
            # Always close the database connection, even if an error occurred
            self.db_handler.close()
    
    def export_pending_actions(self, filename="pending_actions.csv"):
        """
        Exports ONLY pending (incomplete) action items to a CSV file.
        This is useful for seeing what tasks are still left to do.
        
        Args:
            filename: The name of the CSV file to create.
        
        Returns:
            True if successful, False if failed.
        """
        
        # --- Step 1: Connect to the database ---
        if not self.db_handler.connect():
            print("Could not connect to database.")
            return False
        
        # --- Step 2: Fetch only pending actions ---
        # get_pending_actions() uses the aggregation pipeline we built earlier
        pending = self.db_handler.get_pending_actions()
        
        if not pending:
            print("📭 No pending actions found in database.")
            return False
        
        # --- Step 3: Write to CSV ---
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                # For pending actions, we don't need the Meeting ID, just the tasks
                fieldnames = ["Description", "Assignee", "Due Date", "Status"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                
                # Write each pending action as a row
                for action in pending:
                    writer.writerow({
                        "Description": action.get('description', ''),
                        "Assignee": action.get('assignee', 'Unassigned'),
                        "Due Date": action.get('due_date', 'Not specified'),
                        "Status": "Pending"
                    })
            
            print(f"Successfully exported {len(pending)} pending actions to '{filename}'")
            return True
            
        except Exception as e:
            print(f"Failed to export CSV: {e}")
            return False
        
        finally:
            self.db_handler.close()