# scheduler/admin.py
from django.contrib import admin
from .models import MyUser, Note


# Register our model to show in /admin:
class UserAdministration(admin.ModelAdmin):
    # Admin Table UI
    list_display = ("name", "password", "language", "grade")


class NoteAdministration(admin.ModelAdmin):
    # Note Table UI
    list_display = ("title", "msg")


admin.site.register(MyUser, UserAdministration)
admin.site.register(Note, NoteAdministration)
