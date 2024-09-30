from allauth.account.signals import email_confirmed, user_signed_up
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_q.tasks import async_task

from core.tasks import add_email_to_buttondown
from core.models import Profile
from {{ cookiecutter.project_slug }}.utils import get_{{ cookiecutter.project_slug }}_logger

logger = get_{{ cookiecutter.project_slug }}_logger(__name__)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    user = instance
    if user.id == 1:
        user.is_staff = True
        user.is_superuser = True
        user.save()
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


{% if cookiecutter.use_buttondown == 'y' -%}
@receiver(email_confirmed)
def add_email_to_buttondown_on_confirm(sender, **kwargs):
    logger.info(
        "Adding new user to buttondown newsletter, on email confirmation",
        kwargs=kwargs,
        sender=sender,
    )
    async_task(add_email_to_buttondown, kwargs["email_address"], tag="user")
{% endif -%}


{% if cookiecutter.use_buttondown == 'y' and cookiecutter.use_social_auth == 'y' -%}
@receiver(user_signed_up)
def email_confirmation_callback(sender, request, user, **kwargs):
    if 'sociallogin' in kwargs:
        logger.info(
            "Adding new user to buttondown newsletter on social signup",
            kwargs=kwargs,
            sender=sender,
        )
        email = kwargs['sociallogin'].user.email
        if email:
            async_task(add_email_to_buttondown, email, tag="user")
{% endif -%}
