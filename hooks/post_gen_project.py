#!/usr/bin/env python
"""Post-generation hook for cookiecutter-django-saas-starter."""

import os
import shutil
from pathlib import Path


def remove_blog_app():
    """Remove blog app if generate_blog is 'n'."""
    blog_app_path = Path("apps/blog")
    if blog_app_path.exists():
        shutil.rmtree(blog_app_path)
        print("Removed blog app directory")


def remove_blog_templates():
    """Remove blog templates if generate_blog is 'n'."""
    blog_templates_path = Path("frontend/templates/blog")
    if blog_templates_path.exists():
        shutil.rmtree(blog_templates_path)
        print("Removed blog templates directory")


def main():
    """Run post-generation tasks."""
    generate_blog = "{{ cookiecutter.generate_blog }}"

    if generate_blog != "y":
        print("Blog generation disabled, removing blog-related files...")
        remove_blog_app()
        remove_blog_templates()
        print("Blog cleanup complete!")


if __name__ == "__main__":
    main()
