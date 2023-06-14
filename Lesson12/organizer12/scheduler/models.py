from django.db import models
from django.contrib.auth.models import User


class MyUser(models.Model):
    my_user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='myuser')
    language = models.CharField(max_length=100)
    grade = models.CharField(max_length=10)

    def __str__(self):
        return self.my_user.username


class Note(models.Model):
    user_note = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    msg = models.CharField(max_length=100)
    assignee = models.CharField(max_length=100, blank=True)
    e_mail = models.EmailField(max_length=254, blank=True)
