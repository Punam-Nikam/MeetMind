# extractor.py
# THE ULTIMATE VERSION - Catches everything without needing "Action:"

import re
from datetime import datetime, timedelta
from models import ActionItem

# List of known team members we can edit it later.
TEAM_MEMBERS = ["Alice", "Bob", "Charlie", "John", "Jane", "Vishakha", "Siddhi", "Ashwini", "Rahul", "Priya", "Manager", "Client"]

# Common action words
ACTION_WORDS = [
    "communication", "project", "notes", "meet", "client", "submission", 
    "complete", "upgrade", "pending", "fix", "update", "send", "review", 
    "call", "discuss", "schedule", "create", "make", "do", "finish", 
    "work", "start", "submit", "revise", "talk", "email", "write", "read",
    "task", "todo", "action", "need", "must", "should", "please", "help"
]

def parse_due_date(text):
    """Extracts dates from text like '7 July', 'tuesday', 'tomorrow'."""
    text_lower = text.lower()
    
    # 1. YYYY-MM-DD
    match = re.search(r"(\d{4}-\d{2}-\d{2})", text)
    if match:
        return match.group(1)
    
    # 2. DD Month YYYY (e.g., "7 July", "6 july")
    match = re.search(r"(\d{1,2})(?:st|nd|rd|th)?\s+([A-Za-z]+)(?:\s+(\d{4}))?", text_lower)
    if match:
        day = int(match.group(1))
        month_name = match.group(2)
        year = int(match.group(3)) if match.group(3) else datetime.now().year
        months = {"january":1, "february":2, "march":3, "april":4, "may":5, "june":6,
                  "july":7, "august":8, "september":9, "october":10, "november":11, "december":12}
        month = months.get(month_name)
        if month:
            try:
                return datetime(year, month, day).strftime("%Y-%m-%d")
            except:
                pass
    
    # 3. Tomorrow / Today
    if "tomorrow" in text_lower or "tommorow" in text_lower:
        return (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    if "today" in text_lower:
        return datetime.now().strftime("%Y-%m-%d")
    
    # 4. Day names (Monday, Tuesday, etc.)
    days_map = {"monday":0, "tuesday":1, "wednesday":2, "thursday":3, "friday":4, "saturday":5, "sunday":6}
    for day, num in days_map.items():
        if day in text_lower:
            today = datetime.now()
            days_until = (num - today.weekday()) % 7
            if days_until == 0:
                days_until = 7
            return (today + timedelta(days=days_until)).strftime("%Y-%m-%d")
    
    return None

def extract_action_items(text, team_members=None):
    if team_members is None:
        team_members = TEAM_MEMBERS
    
    lines = text.strip().split('\n')
    action_items = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        is_task = False
        
        # --- Rule 1: Contains an action word ---
        for word in ACTION_WORDS:
            if word in line.lower():
                is_task = True
                break
        
        # --- Rule 2: Contains a team member name ---
        if not is_task:
            for member in team_members:
                if member.lower() in line.lower():
                    is_task = True
                    break
        
        # --- Rule 3: Contains a date (like "7 July" or "tuesday") ---
        if not is_task and parse_due_date(line):
            is_task = True
        
        # --- Rule 4: Starts with bullet (-, *, or number like 1.) ---
        if not is_task and re.match(r"^\s*[-*]\s+", line):
            is_task = True
        if not is_task and re.match(r"^\s*\d+\.\s+", line):
            is_task = True
        
        # --- Rule 5: CATCH-ALL: If the line has a dash/hyphen or looks like a note ---
        if not is_task and ('-' in line or ':' in line):
            is_task = True
        
        # If still not a task, SKIP it (to avoid picking up random garbage)
        if not is_task:
            continue
        
        # --- Extract Assignee (Scan the whole line for names) ---
        assignee = None
        for member in team_members:
            if member.lower() in line.lower():
                assignee = member
                break
        
        # --- Extract Due Date ---
        due_date = parse_due_date(line)
        
        # --- Clean Description ---
        raw_desc = line
        # Remove bullet points and numbers
        raw_desc = re.sub(r"^\s*[-*]\s+", "", raw_desc)
        raw_desc = re.sub(r"^\s*\d+\.\s+", "", raw_desc)
        # Remove assignee name from the very start
        if assignee and raw_desc.lower().startswith(assignee.lower()):
            raw_desc = raw_desc[len(assignee):].strip()
        # Clean extra spaces
        raw_desc = re.sub(r'\s+', ' ', raw_desc).strip()
        # Capitalize
        if raw_desc and raw_desc[0].islower():
            raw_desc = raw_desc[0].upper() + raw_desc[1:]
        
        if raw_desc:
            action_items.append(ActionItem(raw_desc, assignee, due_date))
    
    return action_items


if __name__ == "__main__":
    # NOTES
    test_text = """
Communication with ai tool daily
Project submission - 7 July
java notes completion
next meet with client on tuesday
laravel project 3 tasks pending
college stating on 6 july
next client - ashwini
upgrade code
"""
    items = extract_action_items(test_text)
    print("\n" + "="*60)
    print("TESTING EXTRACTOR WITH YOUR NOTES")
    print("="*60)
    for i, item in enumerate(items, 1):
        print(f"{i}. {item.description}")
        print(f"   Assignee: {item.assignee if item.assignee else 'Unassigned'}")
        print(f"   Due Date: {item.due_date if item.due_date else 'Not specified'}")
        print("-"*40)
    print(f"Total extracted: {len(items)}")