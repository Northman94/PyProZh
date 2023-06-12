# scheduler/admin.py
from django.contrib import admin
from .models import Note
from django.contrib.auth.models import User


# Register our model to show in /admin:
# class UserAdministration(admin.ModelAdmin):
#     # Admin Table UI
#     list_display = ("username", "password")
#     # list_display = ("username", "password", "language", "grade")


class NoteAdministration(admin.ModelAdmin):
    # Note Table UI
    list_display = ("title", "msg")


# admin.site.register(User, UserAdministration)
admin.site.register(Note, NoteAdministration)
