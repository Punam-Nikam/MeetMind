from django import forms

class MeetingNoteForm(forms.Form):
    meeting_title = forms.CharField(
        label="Meeting Title",
        max_length=100,
        required=False,
        help_text="E.g., 'Project X Standup' or 'Client Call'"
    )
    note_text = forms.CharField(
        label="Or paste your notes here",
        widget=forms.Textarea(attrs={'rows': 8, 'cols': 80}),
        required=False,
        help_text="Paste your meeting notes directly."
    )
    note_file = forms.FileField(
        label="Or upload a .txt file",
        required=False,
        help_text="Upload a text file containing your meeting notes."
    )

    def clean(self):
        cleaned_data = super().clean()
        note_text = cleaned_data.get('note_text')
        note_file = cleaned_data.get('note_file')

        if not note_text and not note_file:
            raise forms.ValidationError("Please either paste notes or upload a file.")
        return cleaned_data