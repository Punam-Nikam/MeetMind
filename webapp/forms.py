# webapp/forms.py

from django import forms


class MeetingNoteForm(forms.Form):
    """A simple form for uploading meeting notes."""
    meeting_title = forms.CharField(
        label="Meeting Title",
        max_length=100,
        help_text="E.g., 'Project X Standup' or 'Client Call'"
    )
    note_text = forms.CharField(
        label="Paste your meeting notes here:",
        widget=forms.Textarea(attrs={'rows': 10, 'cols': 80}),
        help_text="Write your meeting notes. Use 'Action:' to mark action items."
    )