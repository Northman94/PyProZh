# scheduler/forms.py
# forms.py should contain fields input check
from django import forms
from django.core.exceptions import ValidationError
from .models import Note


class NoteForm(forms.Form):
    title = forms.CharField(max_length=20)
    msg = forms.CharField(max_length=100)

    assignee = forms.CharField(min_length=5, max_length=100)
    e_mail = forms.EmailField()

    def clean_title(self):
        print("CLEAN TITLE")
        data = self.cleaned_data['title']
        if len(data.split(' ')) < 2:
            raise ValidationError("Please create Title with at least two words")
        return data

    def clean(self):
        print("CLEAN")
        cleaned_data = super().clean()
        # NOTE: Everything work with the exchange of the cleaned_data[key] to cleaned_data.get(key)
        title = cleaned_data.get('note_title')
        msg = cleaned_data.get('note_msg')

        if title and msg and (title in msg):
            print(f"Title: {title}")
            print(f"Message: {msg}")
            print(f"Status: {title not in msg}")

            raise ValidationError("Please start your note from the Title")


