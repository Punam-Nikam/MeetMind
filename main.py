# main.py

import time
from reminder import ReminderThread

print("="*60)
print("🚀 MEETMIND - REMINDER SERVICE")
print("="*60)
print("This program starts a background reminder thread.")
print("It will check for pending action items every 10 seconds.")
print("Press Ctrl+C to stop the program.\n")

# Step 1: Create the reminder thread with a 10-second interval (for testing)
# In production, you would use 60 or 300 seconds (5 minutes).
reminder = ReminderThread(interval=10)

# Step 2: Start the background thread
reminder.start()

print("\n💡 The background thread is running. You can continue working.")
print("   Watch the console for reminders!\n")

try:
    # Step 3: Keep the main program alive
    # The main thread just sleeps, while the background thread works.
    while True:
        time.sleep(1)  # Sleep for 1 second, repeat forever
        
except KeyboardInterrupt:
    # Step 4: When the user presses Ctrl+C, stop the thread
    print("\n\nInterrupt received. Shutting down...")
    reminder.stop()
    time.sleep(2)  # Give the thread time to clean up
    print(" Goodbye!")

print("="*60)