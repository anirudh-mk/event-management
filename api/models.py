import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4())
    first_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, unique=True)

    class Meta:
        db_table = 'user'

    @property
    def full_name(self):
        if not self.last_name:
            return self.first_name
        return self.first_name + " " + self.last_name


class Event(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4())
    title = models.CharField(max_length=300)
    description = models.CharField(max_length=500)
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'event'
        ordering = ['created_at']


class Registration(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4())
    event = models.ForeignKey(Event, related_name='registration_event', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='registraiton_user', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'registration'
