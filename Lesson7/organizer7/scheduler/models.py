# scheduler/models.py
from django.db import models


class User(models.Model):
    objects = None
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    grade = models.CharField(max_length=10)

    def __str__(self):
        # Removed Password from Displaying.
        return f"<ul>" \
               f"<li>User: {self.name}</li>" \
               f"<li>Language: {self.language}</li>"\
               f"<li>Grade: {self.grade}</li>" \
               f"</ul>"

