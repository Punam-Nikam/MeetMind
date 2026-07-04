# webapp/views.py

import re
import sys
import os
from django.shortcuts import render
from django.http import HttpResponse
from .forms import MeetingNoteForm

# Add parent directory to Python path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import ActionItem
from database import MongoDBHandler
from extractor import extract_action_items

from django.shortcuts import render, get_object_or_404
from bson import ObjectId  # <-- Add this import at the top

def list_meetings(request):
    db_handler = MongoDBHandler()
    meetings = []
    if db_handler.connect():
        raw_meetings = db_handler.get_all_meetings()
        for m in raw_meetings:
            m['id'] = str(m['_id'])  # Convert ObjectId to string for URL
            meetings.append(m)
        db_handler.close()
    return render(request, 'webapp/list.html', {'meetings': meetings})

def view_meeting(request, meeting_id):
    db_handler = MongoDBHandler()
    meeting = None
    if db_handler.connect():
        # Fetch one document by its ID
        obj_id = ObjectId(meeting_id)
        meeting = db_handler.db.meetings.find_one({'_id': obj_id})
        db_handler.close()
    if not meeting:
        return HttpResponse("Meeting not found.", status=404)
    return render(request, 'webapp/detail.html', {'meeting': meeting})



def upload_notes(request):
    if request.method == 'POST':
        form = MeetingNoteForm(request.POST)
        if form.is_valid():
            note_text = form.cleaned_data['note_text']
            meeting_title = form.cleaned_data['meeting_title']  # <-- Get title
            
                       # Extract action items using our function
            action_items = extract_action_items(note_text)
            
            # --- NEW: Only save if we found actions ---
            saved = False
            meeting_id = None
            if action_items:
                db_handler = MongoDBHandler()
                if db_handler.connect():
                    meeting_id = db_handler.save_meeting(note_text, action_items, meeting_title)
                    db_handler.close()
                    saved = True
            else:
                # If no actions found, show a warning but DON'T save an empty meeting
                print("No actions found, skipping MongoDB save.")
            
            return render(request, 'webapp/results.html', {
                'action_items': action_items,
                'total_actions': len(action_items),
                'saved': saved,
                'meeting_id': meeting_id,
                'note_text': note_text,
                'meeting_title': meeting_title,  # <-- Pass to template
            })
        else:
            return render(request, 'webapp/upload.html', {'form': form})
    
    form = MeetingNoteForm()
    return render(request, 'webapp/upload.html', {'form': form})


# webapp/views.py

def export_csv(request):
    from django.http import HttpResponse
    import csv
    from database import MongoDBHandler
    
    db_handler = MongoDBHandler()
    if not db_handler.connect():
        return HttpResponse("❌ Could not connect to database.", status=500)
    
    meetings = db_handler.get_all_meetings()
    db_handler.close()
    
    if not meetings:
        return HttpResponse("📭 No meetings found in database.", status=404)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="all_actions.csv"'
    
    writer = csv.writer(response)
    # Add "Meeting Title" column
    writer.writerow(['Meeting Title', 'Created At', 'Description', 'Assignee', 'Due Date', 'Status'])
    
    for meeting in meetings:
        meeting_title = meeting.get('meeting_title', 'Untitled')
        created_at = meeting.get('created_at', 'Unknown')
        
        for action in meeting.get('action_items', []):
            writer.writerow([
                meeting_title,
                created_at,
                action.get('description', ''),
                action.get('assignee', 'Unassigned'),
                action.get('due_date', 'Not specified'),
                'Completed' if action.get('is_completed') else 'Pending'
            ])
    
    return response