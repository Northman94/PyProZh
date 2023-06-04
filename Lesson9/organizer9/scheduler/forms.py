# scheduler/forms.py
# forms.py should contain fields input check
from django import forms
from django.core.exceptions import ValidationError
from .models import Note


class NoteForm(forms.Form):
    title = forms.CharField(max_length=20)
    msg = forms.CharField(max_length=100)
    assignee = forms.CharField(max_length=100, required=False)
    e_mail = forms.EmailField(required=False)

    def clean_title(self):
        cln_title = self.cleaned_data["title"]

        if len(cln_title.split(" ")) < 2:
            raise ValidationError("Use at least two words Title")
        return cln_title

    def clean_assignee(self):
        # Whole assignee field:
        cln_assingnee = self.cleaned_data["assignee"]
        # List of words in assignee field:
        words = cln_assingnee.split()

        # This check makes it possible for field to be Optional:
        if cln_assingnee:
            # Amount of Letters in Assignee /or/ Amount of words:
            # if len(cln_assingnee) < 5 or len(words) < 2:
            if words and len(words) < 2:
                raise forms.ValidationError(
                    "Assignee should have at least 2 words"
                    " and be at least 5 characters long."
                )

        for word in words:
            if not word.istitle():
                raise ValidationError(
                    "Each word in the Assignee field" " should be in capital letters."
                )

        return cln_assingnee

    def clean_e_mail(self):
        cln_email = self.cleaned_data["e_mail"]

        if cln_email:
            if "@ithillel.ua" not in cln_email:
                raise ValidationError(
                    "Not a corporate email. Please use an email"
                    ' with the domain "@ithillel.ua".'
                )
        return cln_email

    def clean(self):
        cleaned_data = super().clean()
        cln_assingnee = cleaned_data.get("assignee")
        cln_email = cleaned_data.get("e_mail")

        # if one of fields is not filled:
        if bool(cln_assingnee) != bool(cln_email):
            raise ValidationError("Email or Assignee is not filled properly.")

        return cleaned_data
