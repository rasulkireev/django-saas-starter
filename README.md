To start you'll need to start the Mkdocs server, where a step-by-step process will be provided to you. To do this:
1. `poetry install`
2. `poetry run mkdocs serve`

## Features

- Django 5 and Python 3.11
- User authentication (regular + social) via django-allauth
- Environment variables via django-environ
- TailwindCSS & StimulusJS for frontend via Webpack
- Will work with any DB of your choosing, as long as it is supported by django.
  - Comes with Postgres 17 with pgvector and pg_stat_statements pre-installed
- Local deploy via docker-compose and makefile for rapid local development
- Media storage with any S3 compatible service.
  - Comes with Minio both locally and in prod
- Anymail for email sending with Mailgun (Mailhog for local)
- Structlog for logging setup both for local (console) and prod (json)
- Automated Deployment to Caprover via Github Actions
- Messages handling
  - with nice tempalte component pre-installed
- Sitemaps enabled
- Testing with pytest
- Pre-commit for code quality checks
  - ruff, djlint
- Optimized SEO - Added all the necessary metatags and json-ld schema on all the pages with nice looking OG images.
- API support with django-ninja
- Way to collect feedback pre-installed via a nice widget

Optional Integrations:
- Social Authentication (Github)
- Stripe for payments
- Buttondown for newsletters
- Github Auth for social sign-ins
- Sentry integration
- MJML for email templating
- Logfire for prod and dev logging dashboards

## TODO
- [ ] Drastically improve the documentation structure. Right now everything leaves in the Generated README file.
- [ ] Go from poetry to uv
