# diary/models.py
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    grade = models.IntegerField()

    def __str__(self):
        return self.name
