# Getting Started

This guide will walk you through setting up your Django SaaS project from scratch.

## Prerequisites

Before you begin, make sure you have the following installed:

- Python 3.11 or higher
- Poetry (for Python dependency management)
- Node.js 18 or higher
- Docker and Docker Compose
- Git

## Initial Setup

- First, create your project using cookiecutter:

```bash
cookiecutter gh:rasulkireev/django-saas-starter
```


- You'll be prompted to answer several questions about your project:

      - project_name: Your project's name (e.g., "My Awesome Project")
      - project_slug: A slugified version of your project name (automatically generated)
      - project_description: A brief description of your project
      - Optional integrations (answer 'y' or 'n' for each):
      - use_posthog: PostHog analytics integration
      - use_social_auth: Social authentication
      - use_github_auth: GitHub authentication
      - use_buttondown: Buttondown newsletter integration
      - use_stripe: Stripe payment integration
      - use_opentelemetry: OpenTelemetry tracing
      - use_sentry: Sentry error tracking
      - use_mjml: MJML email templates
      - generate_blog: Blog functionality


- After the project is generated, create and configure your environment variables:

```bash
cd your_project_name
cp .env.example .env
```

- Edit the .env file with your specific configuration values.
