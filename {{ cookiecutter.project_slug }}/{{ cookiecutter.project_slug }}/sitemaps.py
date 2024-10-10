from django.contrib import sitemaps
from django.urls import reverse
from django.contrib.sitemaps import GenericSitemap

{% if cookiecutter.generate_blog == 'y' %}
from core.models import BlogPost
{% endif %}


class StaticViewSitemap(sitemaps.Sitemap):
    """Generate Sitemap for the site"""

    priority = 0.9
    protocol = "https"

    def items(self):
        """Identify items that will be in the Sitemap

        Returns:
            List: urlNames that will be in the Sitemap
        """
        return [
            "home",
            {% if cookiecutter.use_stripe == 'y' -%}
            "pricing",
            {% -endif %}
            {% if cookiecutter.generate_blog == 'y' %}
            "blog_posts",
            {% -endif %}
        ]

    def location(self, item):
        """Get location for each item in the Sitemap

        Args:
            item (str): Item from the items function

        Returns:
            str: Url for the sitemap item
        """
        return reverse(item)

sitemaps = {
    "static": StaticViewSitemap,
    {% if cookiecutter.generate_blog == 'y' %}
    "blog": GenericSitemap(
        {"queryset": BlogPost.objects.all(), "date_field": "created_at"},
        priority=0.85,
        protocol="https",
    ),
    {% -endif %}
