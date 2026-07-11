# webapp/views.py

import re
import sys
import os
from django.shortcuts import render
from django.http import HttpResponse
from .forms import MeetingNoteForm


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import ActionItem
from database import MongoDBHandler
from extractor import extract_action_items

from django.shortcuts import render, get_object_or_404
from bson import ObjectId  

from django.shortcuts import redirect
from django.urls import reverse

def list_meetings(request):
    db_handler = MongoDBHandler()
    meetings = []
    if db_handler.connect():
        raw_meetings = db_handler.get_all_meetings()
        for m in raw_meetings:
            m['id'] = str(m['_id'])  
            meetings.append(m)
        db_handler.close()
    return render(request, 'webapp/list.html', {'meetings': meetings})

def view_meeting(request, meeting_id):
    """
    Displays a single meeting with its action items.
    """
    db_handler = MongoDBHandler()
    meeting = None
    
    if db_handler.connect():
        try:
            from bson import ObjectId
            obj_id = ObjectId(meeting_id)
            meeting = db_handler.db.meetings.find_one({'_id': obj_id})
        except Exception as e:
            print(f"Error fetching meeting: {e}")
        finally:
            db_handler.close()
    
    if not meeting:
        return HttpResponse("Meeting not found.", status=404)
  
    meeting['id'] = str(meeting['_id'])  
    
    return render(request, 'webapp/detail.html', {'meeting': meeting})


def upload_notes(request):
    if request.method == 'POST':
        form = MeetingNoteForm(request.POST, request.FILES)
        if form.is_valid():
            meeting_title = form.cleaned_data.get('meeting_title', 'Untitled Meeting')
            note_text = form.cleaned_data.get('note_text')
            note_file = form.cleaned_data.get('note_file')

            # If a file is uploaded, then we read its content
            if note_file:
                try:
                    note_text = note_file.read().decode('utf-8')
                except Exception as e:
                    note_text = f"Error reading file: {e}"
            # If no file is uploaded, then we use the pasted text from the textarea.
            else:
                note_text = form.cleaned_data.get('note_text')

            # If both are empty, then show error
            if not note_text:
                return render(request, 'webapp/upload.html', {'form': form, 'error': 'No content provided.'})

            action_items = extract_action_items(note_text)

            db_handler = MongoDBHandler()
            saved = False
            meeting_id = None
            if db_handler.connect():
                meeting_id = db_handler.save_meeting(note_text, action_items, meeting_title)
                db_handler.close()
                saved = True

            return render(request, 'webapp/results.html', {
                'action_items': action_items,
                'total_actions': len(action_items),
                'saved': saved,
                'meeting_id': meeting_id,
                'note_text': note_text,
                'meeting_title': meeting_title,
            })
        else:
            return render(request, 'webapp/upload.html', {'form': form})
    else:
        form = MeetingNoteForm()
    return render(request, 'webapp/upload.html', {'form': form})


# webapp/views.py : export to csv file!!

def export_csv(request):
    from django.http import HttpResponse
    import csv
    from database import MongoDBHandler
    
    db_handler = MongoDBHandler()
    if not db_handler.connect():
        return HttpResponse(" Could not connect to database.", status=500)
    
    meetings = db_handler.get_all_meetings()
    db_handler.close()
    
    if not meetings:
        return HttpResponse(" No meetings found in database.", status=404)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="all_actions.csv"'
    
    writer = csv.writer(response)
    # Add "Meeting Title" columns 
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



def mark_complete(request, meeting_id, action_index):
    """
    Marks a specific action item as complete and redirects back to the meeting detail page.
    """
    db_handler = MongoDBHandler()
    success = False
    
    if db_handler.connect():
        success = db_handler.mark_action_complete(meeting_id, action_index)
        db_handler.close()
    
    #  back to the meeting detail page 
    return redirect('view_meeting', meeting_id=meeting_id)