from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Task(models.Model):
    MODERATION_STEP = 1
    APPROVED = 0

    STATUS_CHOICES = [
        (MODERATION_STEP, 'ON moderation'),
        (APPROVED, 'Approved'),
    ]

    title = models.CharField(max_length=255)
    descriptions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
   


    def __str__(self):
        return self.title
    
class TaskLog(models.Model):
    CREATE = 1
    COMPLETE = 2
    DELETE = 3
    ACTION_CHOICES = [
        (CREATE, 'Create'),
        (COMPLETE, 'Complete'),
        (DELETE, 'Delete'),
    ]

    action_data = models.DateTimeField(auto_now_add=True)
    action = models.CharField(choices=ACTION_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    
