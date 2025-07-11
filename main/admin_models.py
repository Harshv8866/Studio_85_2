# studio/admin_models.py or reuse your CustomUser
from django.contrib.auth.models import AbstractUser
from django.db import models

class AdminUser(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)  # store hashed if possible

    def __str__(self):
        return self.username
