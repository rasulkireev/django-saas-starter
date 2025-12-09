from django.contrib import sitemaps
from django.urls import reverse
from django.contrib.sitemaps import GenericSitemap

{% if cookiecutter.generate_blog == 'y' %}
from apps.blog.models import BlogPost
{% endif %}
{% if cookiecutter.generate_docs == 'y' -%}
from apps.docs.views import get_docs_navigation
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
            "landing",
            "uses",
            {% if cookiecutter.use_stripe == 'y' -%}
            "pricing",
            {%- endif %}
            {% if cookiecutter.generate_blog == 'y' %}
            "blog_posts",
            {%- endif %}
        ]

    def location(self, item):
        """Get location for each item in the Sitemap

        Args:
            item (str): Item from the items function

        Returns:
            str: Url for the sitemap item
        """
        return reverse(item)

{% if cookiecutter.generate_docs == 'y' -%}
class DocsSitemap(sitemaps.Sitemap):
    """Generate Sitemap for documentation pages"""

    priority = 0.8
    protocol = "https"
    changefreq = "weekly"

    def items(self):
        """Get all documentation pages from the navigation structure

        Returns:
            List: List of dicts with category and page slugs for each doc page
        """
        doc_pages = []
        navigation = get_docs_navigation()

        for category_info in navigation:
            category_slug = category_info["category_slug"]
            for page_info in category_info["pages"]:
                page_slug = page_info["slug"]
                doc_pages.append(
                    {
                        "category": category_slug,
                        "page": page_slug,
                    }
                )

        return doc_pages

    def location(self, item):
        """Get location for each doc page in the Sitemap

        Args:
            item (dict): Dictionary with category and page slugs

        Returns:
            str: URL for the sitemap item
        """
        return f"/docs/{item['category']}/{item['page']}/"
{% endif %}

sitemaps = {
    "static": StaticViewSitemap,
    {% if cookiecutter.generate_blog == 'y' %}
    "blog": GenericSitemap(
        {"queryset": BlogPost.objects.all(), "date_field": "created_at"},
        priority=0.85,
        protocol="https",
    ),
    {%- endif %}
    {% if cookiecutter.generate_docs == 'y' -%}
    "docs": DocsSitemap,
    {%- endif %}
}
