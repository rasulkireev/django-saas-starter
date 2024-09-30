from django.contrib.auth.models import User
from django.db import models

from core.base_models import BaseModel


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
