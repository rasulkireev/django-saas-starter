from django.db import models
from django.utils import timezone

from core.base_models import BaseModel

class ReferrerBanner(BaseModel):
    referrer = models.CharField(
        max_length=100,
        unique=True,
        help_text="The referrer code from URL parameter (e.g., 'producthunt' from ?ref=producthunt)",  # noqa: E501
    )
    referrer_printable_name = models.CharField(
        max_length=200,
        help_text="Human-readable name to display in banner (e.g., 'Product Hunt')",
    )
    expiry_date = models.DateTimeField(
        null=True, blank=True, help_text="When to stop showing this banner"
    )
    coupon_code = models.CharField(
        max_length=100, blank=True, help_text="Optional discount coupon code"
    )
    discount_amount = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
        help_text="Discount from 0.00 (0%) to 1.00 (100%)",
    )
    is_active = models.BooleanField(
        default=True, help_text="Manually enable/disable banner without deleting it"
    )
    background_color = models.CharField(
        max_length=100,
        default="bg-gradient-to-r from-red-500 to-red-600",
        help_text="Tailwind CSS background color classes (e.g., 'bg-gradient-to-r from-red-500 to-red-600' or 'bg-blue-600')",  # noqa: E501
    )
    text_color = models.CharField(
        max_length=50,
        default="text-white",
        help_text="Tailwind CSS text color class (e.g., 'text-white' or 'text-gray-900')",  # noqa: E501
    )

    def __str__(self):
        return f"{self.referrer_printable_name} ({self.referrer})"

    @property
    def is_expired(self):
        if self.expiry_date is None:
            return False
        return timezone.now() > self.expiry_date

    @property
    def should_display(self):
        return self.is_active and not self.is_expired

    @property
    def discount_percentage(self):
        return int(self.discount_amount * 100)
