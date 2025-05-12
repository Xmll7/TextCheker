from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=255, unique=True)
    address = models.IntegerField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Superuser yaratishda kerakli maydonlar

    def __str__(self):
        return self.email
