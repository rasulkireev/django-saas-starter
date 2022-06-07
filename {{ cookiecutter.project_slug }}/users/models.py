from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    twitter_handle = models.CharField(max_length=20, blank=True)

    class Meta:
        db_table = "auth_user"