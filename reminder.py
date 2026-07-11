# reminder.py  - multithreading reminder system for pending action items

import threading
import time
from database import MongoDBHandler

class ReminderThread:
    """
    A background thread that runs every few seconds to check for pending action items.
    When it finds pending items, it prints a reminder to the console.
    """
    
    def __init__(self, interval=30):
        """
        Initialize the reminder thread.
        
        Args:
            interval: How many seconds to wait between checks (default: 30).
        """
        self.interval = interval
        self.running = False
        self.thread = None
        self.db_handler = None  # Will be created when the thread starts
    
    def start(self):
        """
        Start the background thread.
        This method is called from the main program.
        """
        if self.running:
            print(" Reminder thread is already running.")
            return
        
        self.running = True
        
        # Create a new thread that runs the _run method
        # target=self._run means the thread will execute the _run method
        # daemon=True means the thread will automatically stop when the main program exits
        self.thread = threading.Thread(target=self._run, daemon=True)
        
        # Start the thread
        self.thread.start()
        print(f" Reminder thread started! Checking every {self.interval} seconds.")
    
    def stop(self):
        """
        Stop the background thread.
        Sets the running flag to False, which breaks the loop in _run.
        """
        self.running = False
        print(" Reminder thread stopping...")
    
    def _run(self):
        """
        This is the main loop that runs in the background.
        It runs continuously until the running flag is set to False.
        """
        # Create a database connection specific to this thread
        self.db_handler = MongoDBHandler()
        
        # Connect to the database
        if not self.db_handler.connect():
            print(" Reminder thread: Failed to connect to MongoDB.")
            return
        
        print(" Reminder thread: Connected to MongoDB.")
        
        # Loop while the thread should keep running
        while self.running:
            try:
                # Fetch all pending action items from the database
                pending = self.db_handler.get_pending_actions()
                
             # Inside _run() method, replace the pending loop
                if pending:
                    print("\n" + "="*60)
                    print(" REMINDER: You have pending action items!")
                    print("="*60)
                    
                    for idx, action in enumerate(pending, 1):
                        assignee = action.get('assignee', 'Unassigned')
                        description = action.get('description', 'No description')
                        due_date = action.get('due_date', None)
                        
                        # --- NEW: Check if overdue ---
                        overdue = False
                        if due_date:
                            from datetime import datetime
                            try:
                                due_dt = datetime.strptime(due_date, "%Y-%m-%d")
                                if due_dt < datetime.now():
                                    overdue = True
                            except:
                                pass
                        
                        # Print with OVERDUE tag
                        if overdue:
                            print(f"  {idx}.  {description} (OVERDUE!)")
                        else:
                            print(f"  {idx}. {description}")
                        print(f"      Assigned to: {assignee}")
                        print(f"      Due: {due_date if due_date else 'No due date'}")
                        print("-"*50)
                    
                    print(f" Total pending: {len(pending)}")
                    print("="*60 + "\n")
                else:
                    # No pending items, print a quiet status
                    print(f" [{time.strftime('%H:%M:%S')}] No pending actions found. All clear!")
                
                # Sleep for the specified interval
                time.sleep(self.interval)
                
            except Exception as e:
                # If any error occurs, print it but keep the thread running
                print(f" Reminder thread error: {e}")
                time.sleep(self.interval)
        
        # When the loop exits, close the database connection
        self.db_handler.close()
        print(" Reminder thread stopped.")