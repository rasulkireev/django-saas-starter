from django.contrib.auth.models import User
from django.db import models

from core.base_models import BaseModel
from core.utils import generate_random_key


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=10, unique=True, default=generate_random_key)
