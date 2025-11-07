---
title: Getting Started with {{ cookiecutter.project_name }}
description: Learn how to get started with {{ cookiecutter.project_name }}, {{ cookiecutter.project_description }}
keywords: {{ cookiecutter.project_name }}, getting started, documentation
author: {{ cookiecutter.author_name }}
---

Welcome to {{ cookiecutter.project_name }}! This guide will help you get started with your new Django SaaS application.

## What is {{ cookiecutter.project_name }}?

{{ cookiecutter.project_name }} is built on a modern Django SaaS starter template that includes:

- User authentication and profile management
- {% if cookiecutter.use_stripe == 'y' -%}Subscription billing with Stripe{% endif %}
- {% if cookiecutter.generate_blog == 'y' -%}Built-in blog system with markdown support{% endif %}
- {% if cookiecutter.use_posthog == 'y' -%}Product analytics with PostHog{% endif %}
- {% if cookiecutter.use_s3 == 'y' -%}Cloud storage with S3{% endif %}
- Responsive design with Tailwind CSS
- API endpoints with Django Ninja
- {% if cookiecutter.use_sentry == 'y' -%}Error tracking with Sentry{% endif %}

## Next Steps

Ready to [get started](/docs/getting-started/quickstart)? Sign up for an account and explore the features!
