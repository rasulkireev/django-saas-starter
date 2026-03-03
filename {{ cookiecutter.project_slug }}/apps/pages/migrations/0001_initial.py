from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ReferrerBanner",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "referrer",
                    models.CharField(
                        help_text="The referrer code from URL parameter (e.g., 'producthunt' from ?ref=producthunt)",
                        max_length=100,
                        unique=True,
                    ),
                ),
                (
                    "referrer_printable_name",
                    models.CharField(
                        help_text="Human-readable name to display in banner (e.g., 'Product Hunt')",
                        max_length=200,
                    ),
                ),
                (
                    "expiry_date",
                    models.DateTimeField(blank=True, help_text="When to stop showing this banner", null=True),
                ),
                (
                    "coupon_code",
                    models.CharField(blank=True, help_text="Optional discount coupon code", max_length=100),
                ),
                (
                    "discount_amount",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        help_text="Discount from 0.00 (0%) to 1.00 (100%)",
                        max_digits=3,
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Manually enable/disable banner without deleting it",
                    ),
                ),
                (
                    "background_color",
                    models.CharField(
                        default="bg-gradient-to-r from-red-500 to-red-600",
                        help_text="Tailwind CSS background color classes (e.g., 'bg-gradient-to-r from-red-500 to-red-600' or 'bg-blue-600')",
                        max_length=100,
                    ),
                ),
                (
                    "text_color",
                    models.CharField(
                        default="text-white",
                        help_text="Tailwind CSS text color class (e.g., 'text-white' or 'text-gray-900')",
                        max_length=50,
                    ),
                ),
            ],
        )
    ]
