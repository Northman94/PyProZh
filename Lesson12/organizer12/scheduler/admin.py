# scheduler/admin.py
from django.contrib import admin
from .models import MyUser, Note
from django.contrib.auth.models import User


# Register our model to show in /admin:
class UserAdministration(admin.ModelAdmin):
    # Admin Table UI
    list_display = ("username", "password")


class MyUserAdministration(admin.ModelAdmin):
    list_display = ("language", "grade")


class NoteAdministration(admin.ModelAdmin):
    # Note Table UI
    list_display = ("title", "msg")


admin.site.register(MyUser, MyUserAdministration)
admin.site.register(Note, NoteAdministration)

# admin.site.register(User, UserAdministration)
# No need to register User as it is already registered UnderTheHood
