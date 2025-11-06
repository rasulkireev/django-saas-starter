import re
import uuid

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model

from core.choices import EmailType
from core.utils import track_email_sent
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

        logger.info(
            "[Send Confirmation Mail] Sending email",
            signup=signup,
            email_type=email_type,
            user_id=emailconfirmation.email_address.user.id,
            email=emailconfirmation.email_address.email,
        )

        try:
            result = super().send_confirmation_mail(request, emailconfirmation, signup)
            track_email_sent(
                email_address=emailconfirmation.email_address.email,
                email_type=email_type,
                profile=profile,
            )
            return result
        except Exception as error:
            logger.error(
                "[Send Confirmation Mail] Failed to send email",
                error=str(error),
                exc_info=True,
                user_id=emailconfirmation.email_address.user.id,
                email=emailconfirmation.email_address.email,
            )
            raise

    def send_mail(self, template_prefix, email, context):
        """
        Override to prevent sending password reset emails for non-existent accounts.
        This is a security best practice - we still show a success message to users,
        but we don't actually send an email if the account doesn't exist.

        For password reset flows, django-allauth uses these template prefixes:
        - 'account/email/password_reset_key' - when account exists
        - 'account/email/unknown_account' - when account doesn't exist (we suppress this)
        - 'account/email/account_already_exists' - when trying to sign up with existing email

        Args:
            template_prefix: The email template prefix
            email: The recipient email address
            context: Template context dictionary
        """
        # Don't send email for unknown accounts during password reset
        if template_prefix == "account/email/unknown_account":
            logger.info(
                "[Send Mail] Suppressing unknown account email for security",
                email=email,
                template_prefix=template_prefix,
            )
            return

        # For all other emails, proceed normally
        logger.info(
            "[Send Mail] Sending email",
            email=email,
            template_prefix=template_prefix,
        )

        try:
            return super().send_mail(template_prefix, email, context)
        except Exception as error:
            logger.error(
                "[Send Mail] Failed to send email",
                error=str(error),
                exc_info=True,
                email=email,
                template_prefix=template_prefix,
            )
            raise


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
