from django.db import models
from django.contrib.auth.models import User

class Members(models.Model):
    title = models.CharField(max_length=255)
    descriptions = models.TextField(blank=True)



    def __str__(self):
        return self.title



