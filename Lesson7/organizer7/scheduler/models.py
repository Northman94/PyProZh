# scheduler/models.py
from django.db import models


class User(models.Model):
    objects = None
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    grade = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Note(models.Model):
    # Cascade deleted all Obj with no relations
    user_note = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    msg = models.CharField(max_length=250)
