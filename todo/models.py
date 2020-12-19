from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)                         # blank = True => Can be empty
    created = models.DateTimeField(auto_now_add=True)           # Not editable
    datecompleted = models.DateTimeField(null=True, blank=True)             # Allow it to be null.
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)    # Foregin key

    def __str__(self):
        return self.title
