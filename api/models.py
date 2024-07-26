import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4())

    class Meta:
        db_table = 'user'


class Event(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4())
    title = models.CharField(max_length=300)
    description = models.CharField(max_length=500)
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'event'
        ordering = ['created_at']
