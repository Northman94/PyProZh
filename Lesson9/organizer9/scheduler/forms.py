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
        cln_title = self.cleaned_data['title']

        if len(cln_title.split(' ')) < 2:
            raise ValidationError("Use two words Title")
        return cln_title

    def clean_assignee(self):
        cln_assingnee = self.cleaned_data['assignee']

        if len(cln_assingnee.split(' ')) < 2:
            raise ValidationError("Put at least 2 words.")

        words = cln_assingnee.split()
        for word in words:
            print(f"Whole Capitl: {words}")
            print(f"Capital: {word}")
            if not word[0].isupper():
                print(f"WORD IS UPPER: {word[0].isupper()}")
                raise ValidationError("Each word in the Assignee field should be in capital letters.")

        return cln_assingnee

    def clean_e_mail(self):
        cln_email = self.cleaned_data['e_mail']

        if "@ithillel.ua" not in cln_email:
            raise ValidationError("Not a corporate email. Please use an email with the domain \"@ithillel.ua\".")

        return cln_email


    # def clean(self):
    #     print("CLEAN")
    #     cleaned_data = super().clean()
    #
    #     cln_title = cleaned_data.get('title')
    #     cln_msg = cleaned_data.get('msg')
    #     cln_assingnee = cleaned_data.get('assignee')
    #     cln_email = cleaned_data.get('e_mail')
    #
    #     if not cln_title or not cln_msg:
    #         print(f"cln_title: {cln_title}")
    #         print(f"cln_msg: {cln_msg}")
    #
    #         raise ValidationError("Title & Message are not meeting Requirements. ")
    #
    #     # if one of fields is not filled:
    #     if bool(cln_assingnee) != bool(cln_email):
    #         print(f"ass: {bool(cln_assingnee)}")
    #         print(f"mail: {bool(cln_email)}")
    #         raise ValidationError("You missed Email or Assignee.")
    #
    #     return cleaned_data

