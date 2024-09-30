from allauth.account.signals import email_confirmed
from allauth.socialaccount.signals import social_account_added
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_q.tasks import async_task

from core.tasks import add_email_to_buttondown
from core.models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

{% if cookiecutter.use_buttondown == 'y' -%}
@receiver(email_confirmed)
{% if cookiecutter.use_social_auth == 'y' -%}
@receiver(social_account_added)
{% endif -%}
def email_confirmation_callback(sender, **kwargs):
    if 'email_address' in kwargs:
        # This is for email_confirmed signal
        email = kwargs['email_address']
    {% if cookiecutter.use_social_auth == 'y' -%}
    elif 'sociallogin' in kwargs:
        # This is for social_account_added signal
        email = kwargs['sociallogin'].user.email
    {% endif -%}
    else:
        # If neither email_address nor sociallogin is present, we can't proceed
        return

    if email:
        async_task(add_email_to_buttondown, email, tag="user")
{% endif -%}
