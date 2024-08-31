from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Profile(models.Model):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('client', 'Client'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)

    def __str__(self):
        return self.name

class Task(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.BooleanField(default=False)  # True for completed, False for pending

    def __str__(self):
        return self.title

class ActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    endpoint = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} accessed {self.endpoint} with {self.method}"
