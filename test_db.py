# test_db.py

from database import MongoDBHandler

# Create handler (reads MONGO_URI from .env automatically)
db = MongoDBHandler()

# Connect
db.connect()

# Get all meetings
meetings = db.get_all_meetings()

print("\n" + "="*60)
print("📁 ALL MEETINGS IN DATABASE")
print("="*60)

for meeting in meetings:
    print(f"\n📅 Meeting (ID: {meeting['_id']})")
    print(f"   📝 Text: {meeting['meeting_text'][:50]}...")
    print(f"   📋 Actions: {meeting['total_actions']}")
    print(f"   🕐 Created: {meeting['created_at']}")

db.close()