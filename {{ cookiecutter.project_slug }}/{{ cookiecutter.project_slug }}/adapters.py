import re
import uuid

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model

from apps.core.choices import EmailType
from apps.core.utils import send_transactional_email
from {{ cookiecutter.project_slug }}.utils import get_{{ cookiecutter.project_slug }}_logger

logger = get_{{ cookiecutter.project_slug }}_logger(__name__)

User = get_user_model()


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Custom adapter to track email confirmations and welcome emails.
    """

    def send_confirmation_mail(self, request, emailconfirmation, signup):
        """
        Override to track email confirmation sends.

        Args:
            request: The HTTP request
            emailconfirmation: The email confirmation object
            signup: Boolean indicating if this is during signup (True) or resend (False)
        """
        profile = (
            emailconfirmation.email_address.user.profile
            if hasattr(emailconfirmation.email_address.user, "profile")
            else None
        )

        # Track as welcome email during signup, confirmation email on resend
        email_type = EmailType.WELCOME if signup else EmailType.EMAIL_CONFIRMATION
        email_address = emailconfirmation.email_address.email
        context = {
            "flow": "signup" if signup else "confirmation_resend",
            "user_id": emailconfirmation.email_address.user.id,
        }

        logger.info(
            "[Send Confirmation Mail] Sending email",
            signup=signup,
            email_type=email_type,
            user_id=emailconfirmation.email_address.user.id,
            email=email_address,
        )

        success = send_transactional_email(
            lambda: super(CustomAccountAdapter, self).send_confirmation_mail(
                request,
                emailconfirmation,
                signup,
            ),
            email_address=email_address,
            email_type=email_type,
            profile=profile,
            context=context,
        )

        if not success:
            logger.warning(
                "[Send Confirmation Mail] Email send failed after retries",
                signup=signup,
                email_type=email_type,
                user_id=emailconfirmation.email_address.user.id,
                email=email_address,
            )


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom adapter to automatically generate usernames from email addresses
    during social authentication signup, bypassing the username selection page.
    """

    def populate_user(self, request, sociallogin, data):
        """
        Automatically set username from email address before user creation.
        Uses the part before @ symbol as username, ensuring uniqueness.
        """
        user = super().populate_user(request, sociallogin, data)

        if not user.username and user.email:
            base_username = re.sub(r"[^\w]", "", user.email.split("@")[0])
            if not base_username:
                base_username = f"user{uuid.uuid4().hex[:8]}"
            username = base_username

            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1

            user.username = username

        return user
