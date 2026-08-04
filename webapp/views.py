import re
import sys
import os
import traceback
from django.shortcuts import render, redirect
from django.http import HttpResponse  
from django.urls import reverse
from .forms import MeetingNoteForm
from database import MongoDBHandler
from extractor import extract_action_items
from bson import ObjectId  


def upload_notes(request):
    if request.method == 'POST':
        form = MeetingNoteForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                meeting_title = form.cleaned_data.get('meeting_title', 'Untitled Meeting')
                note_text = form.cleaned_data.get('note_text')
                note_file = form.cleaned_data.get('note_file')

                if note_file:
                    try:
                        note_text = note_file.read().decode('utf-8')
                    except Exception as e:
                        return HttpResponse(f"Error reading file: {e}", status=400)

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
            except Exception as e:
                # Safety net to catch errors
                return HttpResponse(f"<h1>DEBUG ERROR</h1><pre>{traceback.format_exc()}</pre>", status=500)
        else:
            return render(request, 'webapp/upload.html', {'form': form})
    else:
        form = MeetingNoteForm()
    return render(request, 'webapp/upload.html', {'form': form})


def list_meetings(request):
    import os
    if os.environ.get('ENV') == 'production':
        return HttpResponse("🔒 This page is private. Please contact the developer for access.", status=404)
    
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
    db_handler = MongoDBHandler()
    meeting = None
    if db_handler.connect():
        try:
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
        return HttpResponse("📭 No meetings found in database.", status=404)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="all_actions.csv"'
    
    writer = csv.writer(response)
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
    db_handler = MongoDBHandler()
    success = False
    if db_handler.connect():
        success = db_handler.mark_action_complete(meeting_id, action_index)
        db_handler.close()
    return redirect('view_meeting', meeting_id=meeting_id)