from django.db import models


class BlogPostStatus(models.TextChoices):
    DRAFT = "draft"
    PUBLISHED = "published"
