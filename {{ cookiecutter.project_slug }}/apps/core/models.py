from decimal import Decimal, InvalidOperation


from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.conf import settings
from django_q.tasks import async_task

from apps.core.base_models import BaseModel
from apps.core.choices import ProfileStates, EmailType
from apps.core.model_utils import generate_random_key


from {{ cookiecutter.project_slug }}.utils import get_{{ cookiecutter.project_slug }}_logger

logger = get_{{ cookiecutter.project_slug }}_logger(__name__)


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=30, unique=True, default=generate_random_key)

    {% if cookiecutter.use_stripe == 'y' %}
    stripe_subscription_id = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="The user's Stripe subscription id, if it exists",
    )
    stripe_customer_id = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="The user's Stripe customer id, if it exists",
    )
    {% endif %}

    state = models.CharField(
        max_length=255,
        choices=ProfileStates.choices,
        default=ProfileStates.STRANGER,
        help_text="The current state of the user's profile",
    )

    def track_state_change(self, to_state, metadata=None, source_function=None):
        async_task(
            "apps.core.tasks.track_state_change",
            profile_id=self.id,
            from_state=self.current_state,
            to_state=to_state,
            metadata=metadata,
            source_function=source_function,
            group="Track State Change",
        )

    @property
    def current_state(self):
        if not self.state_transitions.all().exists():
            return ProfileStates.STRANGER
        latest_transition = self.state_transitions.latest("created_at")
        return latest_transition.to_state

    {% if cookiecutter.use_stripe == 'y' %}
    @property
    def has_active_subscription(self):
        return self.state in [
            ProfileStates.SUBSCRIBED,
            ProfileStates.CANCELLED,
        ] or (self.user.is_superuser and settings.ENVIRONMENT == "prod")
    {% endif %}
class ProfileStateTransition(BaseModel):
    profile = models.ForeignKey(
        Profile,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="state_transitions",
    )
    from_state = models.CharField(max_length=255, choices=ProfileStates.choices)
    to_state = models.CharField(max_length=255, choices=ProfileStates.choices)
    backup_profile_id = models.IntegerField()
    metadata = models.JSONField(null=True, blank=True)

class Feedback(BaseModel):
    profile = models.ForeignKey(
        Profile,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="feedback",
        help_text="The user who submitted the feedback",
    )
    feedback = models.TextField(
        help_text="The feedback text",
    )
    page = models.CharField(
        max_length=255,
        help_text="The page where the feedback was submitted",
    )

    def __str__(self):
        return f"{self.profile.user.email}: {self.feedback}"

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)

        if is_new:
            from django.conf import settings
            from django.core.mail import send_mail

            from apps.core.utils import track_email_sent

            subject = "New Feedback Submitted"
            message = f"""
                New feedback was submitted:\n\n
                User: {self.profile.user.email if self.profile else "Anonymous"}
                Feedback: {self.feedback}
                Page: {self.page}
            """
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [settings.DEFAULT_FROM_EMAIL]

            send_mail(subject, message, from_email, recipient_list, fail_silently=True)

            for recipient_email in recipient_list:
                track_email_sent(
                    email_address=recipient_email,
                    email_type=EmailType.FEEDBACK_NOTIFICATION,
                    profile=self.profile,
                )

class EmailSent(BaseModel):
    email_address = models.EmailField(help_text="The recipient email address")
    email_type = models.CharField(
        max_length=50, choices=EmailType.choices, help_text="Type of email sent"
    )
    profile = models.ForeignKey(
        Profile,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="emails_sent",
        help_text="Associated user profile, if applicable",
    )

    class Meta:
        verbose_name = "Email Sent"
        verbose_name_plural = "Emails Sent"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.email_type} to {self.email_address}"
