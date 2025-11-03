def referrer_banner(request):
    """
    Adds referrer banner to context if ref parameter is provided and a matching banner exists.
    Banner is only shown if it's active and not expired.
    """
    from core.models import ReferrerBanner

    referrer_code = request.GET.get("ref")
    if referrer_code:
        try:
            banner = ReferrerBanner.objects.get(referrer=referrer_code)
            if banner.should_display:
                return {"referrer_banner": banner}
        except ReferrerBanner.DoesNotExist:
            pass

    return {}
