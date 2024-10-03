from django.contrib.auth.models import User
from django.db import models

from core.base_models import BaseModel
from core.utils import generate_random_key
from {{ cookiecutter.project_slug }}.utils import get_{{ cookiecutter.project_slug }}_logger

logger = get_{{ cookiecutter.project_slug }}_logger(__name__)


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=10, unique=True, default=generate_random_key)

    {% if cookiecutter.use_stripe == 'y' %}
    subscription = models.ForeignKey(
        "djstripe.Subscription",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="profile",
        help_text="The user's Stripe Subscription object, if it exists",
    )
    customer = models.ForeignKey(
        "djstripe.Customer",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="profile",
        help_text="The user's Stripe Customer object, if it exists",
    )

    def track_state_change(self, to_state, metadata=None):
        from_state = self.current_state

        if from_state != to_state:
            logger.info(
                "Tracking State Change", from_state=from_state, to_state=to_state, profile_id=self.id, metadata=metadata
            )
            ProfileStateTransition.objects.create(
                profile=self, from_state=from_state, to_state=to_state, backup_profile_id=self.id, metadata=metadata
            )

    @property
    def current_state(self):
        if not self.state_transitions.all().exists():
            return ProfileStates.STRANGER
        latest_transition = self.state_transitions.latest("created_at")
        return latest_transition.to_state


class ProfileStates(models.TextChoices):
    STRANGER = "stranger"
    SIGNED_UP = "signed_up"
    SUBSCRIBED = "subscribed"
    CANCELLED = "cancelled"
    CHURNED = "churned"
    ACCOUNT_DELETED = "account_deleted"


class ProfileStateTransition(BaseModel):
    profile = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL, related_name="state_transitions")
    from_state = models.CharField(max_length=255, choices=ProfileStates.choices)
    to_state = models.CharField(max_length=255, choices=ProfileStates.choices)
    backup_profile_id = models.IntegerField()
    metadata = models.JSONField(null=True, blank=True)

{% endif %}
