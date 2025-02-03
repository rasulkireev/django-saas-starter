To start you'll need to start the Mkdocs server, where a step-by-step process will be provided to you. To do this:
1. `poetry install`
2. `poetry run mkdocs serve`

## Features

- Django 5 and Python 3.11
- User authentication (regular + social) via django-allauth
- Environment variables via django-environ
- TailwindCSS & StimulusJS for frontend via Webpack
- Will work with any DB of your choosing, as long as it is supported by django. (postgres 15 with pgvector installed for local dev)
- Local deploy via docker-compose and makefile for rapid local development
- Media storage with any S3 compatible service. I use Minio both locally and in prod
- Anymail for email sending with Mailgun (Mailhog for local)
- Structlog for logging setup both for local (console) and prod (json)
- Automated Deployment to Caprover via Github Actions
- Messages handling
- Sitemaps enabled
- Testing with pytest
- Pre-commit for code quality checks
- Optimized SEO - Added all the necessary metatags and json-ld schema on all the pages with nice looking OG images.
- API support with django-ninja

Optional Integrations:
- Social Authentication (Github)
- Stripe for payments
- Buttondown for newsletters
- Github Auth for social sign-ins
- Sentry integration
- OpenTelemetry for tracing (Signoz in this case)

## Roadmap
- Drastically improve the documentation structure. Right now everything leaves in the Generated README file.
- MJML
