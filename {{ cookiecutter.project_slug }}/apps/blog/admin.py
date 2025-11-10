{% if cookiecutter.generate_blog == 'y' %}
from django.contrib import admin

from apps.blogmodels import BlogPost

admin.site.register(BlogPost)
{% endif %}
