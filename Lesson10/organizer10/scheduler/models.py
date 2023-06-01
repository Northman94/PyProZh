# scheduler/models.py
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# class MyUserManager(BaseUserManager):
#     def create_user(self, username, password=None, **extra_fields):
#         extra_fields.setdefault('is_superuser', False)
#         user = self.model(username=username, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, username, password=None, **extra_fields):
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('is_staff', True)
#         return self.create_user(username, password, **extra_fields)



class MyUser(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    grade = models.CharField(max_length=10)

    # objects = MyUserManager()  # Associate the custom manager

    def __str__(self):
        return self.name


class Note(models.Model):
    # ForeignKey is a link to certain User in another table
    # (.CASCADE) will Delete all Obj-s with no relations
    user_note = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    title = models.CharField(max_length=20)
    msg = models.CharField(max_length=100)

    assignee = models.CharField(max_length=100, blank=True)
    e_mail = models.EmailField(max_length=254, blank=True)



