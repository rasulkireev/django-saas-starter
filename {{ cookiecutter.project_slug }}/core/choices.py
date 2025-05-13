from django.db import models

{% if cookiecutter.use_stripe == 'y' %}
class ProfileStates(models.TextChoices):
    STRANGER = "stranger"
    SIGNED_UP = "signed_up"
    SUBSCRIBED = "subscribed"
    CANCELLED = "cancelled"
    CHURNED = "churned"
    ACCOUNT_DELETED = "account_deleted"
{% endif %}

{% if cookiecutter.generate_blog == 'y' %}
class BlogPostStatus(models.TextChoices):
    DRAFT = "draft"
    PUBLISHED = "published"
{% endif %}
