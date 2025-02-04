# Django SaaS Starter

Welcome to the documentation for mty Django SaaS Starter! This is a modern Django SaaS starter template that provides a solid foundation for building your next web application.

## Core Features

- **Django 5 and Python 3.11** - Latest stable versions for robust backend development
- **Modern Authentication** - Complete user authentication system via django-allauth
- **Frontend Stack** - TailwindCSS & StimulusJS via Webpack
- **Database Flexibility** - Works with any Django-supported database (PostgreSQL 15 with pgvector for local dev)
- **Development Environment** - Docker-compose and Makefile for rapid local development
- **Storage Solution** - Media storage with any S3 compatible service (Minio for local/prod)
- **Email Integration** - Anymail with Mailgun (Mailhog for local development)
- **Logging** - Structlog setup for both local (console) and prod (json)
- **Deployment** - Automated deployment to Caprover via Github Actions
- **Testing** - Ready to go with pytest
- **Code Quality** - Pre-commit hooks for maintaining code standards
- **SEO Optimization** - Complete meta tags and JSON-LD schema
- **API Support** - Built-in API capabilities with django-ninja

## Optional Integrations

The template includes several optional integrations that can be enabled during project creation:

- Social Authentication (Github)
- Stripe Payments
- Buttondown Newsletter Integration
- Sentry Error Tracking
- OpenTelemetry Tracing (with Signoz)
- MJML Email Templates
- Blog Functionality
