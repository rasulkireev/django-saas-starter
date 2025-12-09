from django.contrib import admin

from .models import ReferrerBanner


@admin.register(ReferrerBanner)
class ReferrerBannerAdmin(admin.ModelAdmin):
    list_display = (
        "referrer",
        "referrer_printable_name",
        "discount_percentage",
        "coupon_code",
        "expiry_date",
        "is_active",
        "should_display",
    )
    list_filter = ("is_active", "expiry_date")
    search_fields = ("referrer", "referrer_printable_name", "coupon_code")
    readonly_fields = ("created_at", "updated_at", "is_expired", "should_display")
    fieldsets = (
        (
            "Banner Information",
            {
                "fields": (
                    "referrer",
                    "referrer_printable_name",
                    "is_active",
                )
            },
        ),
        (
            "Design",
            {
                "fields": (
                    "background_color",
                    "text_color",
                ),
                "description": "Customize banner appearance using Tailwind CSS classes",
            },
        ),
        (
            "Discount Details",
            {
                "fields": (
                    "discount_amount",
                    "coupon_code",
                    "expiry_date",
                )
            },
        ),
        (
            "Status",
            {
                "fields": (
                    "is_expired",
                    "should_display",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
