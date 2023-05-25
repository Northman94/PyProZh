# scheduler/models.py
from django.db import models


class MyUser(models.Model):
    objects = None
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    grade = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Note(models.Model):
    objects = None
    # ForeignKey is a link to certain User in another table
    # Cascade will delete all Obj with no relations
    user_note = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    msg = models.CharField(max_length=250)
