import re
from models import ActionItem
from database import MongoDBHandler


CONNECTION_STRING ="MONGO_URI"


meeting_notes = """
Meeting about Project X
Attendees: Alice, Bob, Charlie
Action: Alice will update the design by tomorrow.
Action: Bob to send the report @Bob due 2026-06-30
Charlie mentioned the server is slow.
Action: Charlie restart the server.
"""

# Find all action lines
pattern = r"^Action:.*"
action_lines = re.findall(pattern, meeting_notes, re.MULTILINE)

# List to store our ActionItem objects
action_items = []

print("\n" + "="*70)
print("📝 MEETMIND - ACTION ITEM EXTRACTOR")
print("="*70)

for line in action_lines:
    # Remove "Action: " prefix to get description
    description = line.replace("Action: ", "", 1).strip()
    
    # Find @name
    name_pattern = r"@(\w+)"
    name_match = re.search(name_pattern, line)
    
    assignee = None
    
    if name_match:
        assignee = name_match.group(1)
    else:
        first_word = description.split()[0] if description else ""
        team_members = ["Alice", "Bob", "Charlie"]
        
        if first_word in team_members:
            assignee = first_word
    
    # Find due date
    date_pattern = r"(\d{4}-\d{2}-\d{2})"
    date_match = re.search(date_pattern, line)
    due_date = date_match.group(1) if date_match else None
    
    # Create ActionItem object
    item = ActionItem(description, assignee, due_date)
    action_items.append(item)

# --- Print the table ---
print("\n" + "-"*70)
print("📋 EXTRACTED ACTION ITEMS")
print("-"*70)
print(f"{'Status':<6} {'Assignee':<14} {'Due Date':<15} {'Description'}")
print("-"*70)

for item in action_items:
    print(item)

print("-"*70)
print(f"✅ Total action items extracted: {len(action_items)}")
print("="*70 + "\n")

# --- NEW: SAVE TO MONGODB ---
print("\n" + "-"*70)
print("💾 SAVING TO MONGODB ATLAS")
print("-"*70)

# Create a database handler
db_handler = MongoDBHandler()

if db_handler.connect():
    # Save the meeting and action items
    meeting_id = db_handler.save_meeting(meeting_notes, action_items)
    
    if meeting_id:
        print(f"📌 Meeting ID: {meeting_id}")
        
        # Show pending actions from the database
        print("\n📋 Fetching pending actions from database...")
        pending = db_handler.get_pending_actions()
        for p in pending:
            print(f"   - {p['description']} (Assigned to: {p['assignee']})")
else:
    print("❌ Could not save to MongoDB. Check your connection string.")

# Close the database connection
db_handler.close()
print("="*70 + "\n")