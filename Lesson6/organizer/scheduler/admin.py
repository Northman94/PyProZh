# scheduler/admin.py
from django.contrib import admin
from .models import User
# Register our model to show in /admin:


class UserAdministration(admin.ModelAdmin):
    # Admin Table UI
    list_display = ('name', 'password', "language", "grade")


admin.site.register(User, UserAdministration)

