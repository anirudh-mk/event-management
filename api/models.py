import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4())

    class Meta:
        db_table = 'user'
