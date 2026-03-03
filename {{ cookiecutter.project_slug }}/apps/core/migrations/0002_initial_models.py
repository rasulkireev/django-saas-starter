from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid

import apps.core.model_utils


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_enable_extensions"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("key", models.CharField(default=apps.core.model_utils.generate_random_key, max_length=30, unique=True)),
                (
                    "state",
                    models.CharField(
                        choices=[
                            ("stranger", "Stranger"),
                            ("cold", "Cold"),
                            ("warm", "Warm"),
                            ("hot", "Hot"),
                            ("customer", "Customer"),
                        ],
                        default="stranger",
                        help_text="The current state of the user's profile",
                        max_length=255,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProfileStateTransition",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "from_state",
                    models.CharField(
                        choices=[
                            ("stranger", "Stranger"),
                            ("cold", "Cold"),
                            ("warm", "Warm"),
                            ("hot", "Hot"),
                            ("customer", "Customer"),
                        ],
                        max_length=255,
                    ),
                ),
                (
                    "to_state",
                    models.CharField(
                        choices=[
                            ("stranger", "Stranger"),
                            ("cold", "Cold"),
                            ("warm", "Warm"),
                            ("hot", "Hot"),
                            ("customer", "Customer"),
                        ],
                        max_length=255,
                    ),
                ),
                ("backup_profile_id", models.IntegerField()),
                ("metadata", models.JSONField(blank=True, null=True)),
                (
                    "profile",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="state_transitions",
                        to="core.profile",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Feedback",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("feedback", models.TextField(help_text="The feedback text")),
                ("page", models.CharField(help_text="The page where the feedback was submitted", max_length=255)),
                (
                    "profile",
                    models.ForeignKey(
                        blank=True,
                        help_text="The user who submitted the feedback",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="feedback",
                        to="core.profile",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EmailSent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("email_address", models.EmailField(help_text="The recipient email address", max_length=254)),
                (
                    "email_type",
                    models.CharField(
                        choices=[
                            ("welcome", "Welcome"),
                            ("email_confirmation", "Email Confirmation"),
                            ("feedback_notification", "Feedback Notification"),
                        ],
                        help_text="Type of email sent",
                        max_length=50,
                    ),
                ),
                (
                    "profile",
                    models.ForeignKey(
                        blank=True,
                        help_text="Associated user profile, if applicable",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="emails_sent",
                        to="core.profile",
                    ),
                ),
            ],
            options={
                "verbose_name": "Email Sent",
                "verbose_name_plural": "Emails Sent",
                "ordering": ["-created_at"],
            },
        ),
    ]
