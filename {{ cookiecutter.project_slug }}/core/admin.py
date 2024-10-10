{% if cookiecutter.generate_blog == 'y' %}
from django.contrib import admin

from core.models import BlogPost

admin.site.register(BlogPost)
{% endif %}
