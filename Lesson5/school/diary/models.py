from django.db import models

class Student(models.Model):
    username = models.CharField(max_length=20)
    language = models.CharField(max_length=20)
    grade = models.IntegerField()
