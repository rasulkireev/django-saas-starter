{% if cookiecutter.generate_blog == 'y' %}
from django.contrib import admin

from blog.models import BlogPost

admin.site.register(BlogPost)
{% endif %}
