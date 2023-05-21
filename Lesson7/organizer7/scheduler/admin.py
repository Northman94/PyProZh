# scheduler/admin.py
from django.contrib import admin
from .models import User, Note


# Register our model to show in /admin:
class UserAdministration(admin.ModelAdmin):
    # Admin Table UI
    list_display = ('name', 'password', "language", "grade")


class NoteAdministration(admin.ModelAdmin):
    list_display = ('title', 'msg')


admin.site.register(User, UserAdministration)
admin.site.register(Note, NoteAdministration)
