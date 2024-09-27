To start you'll need to start the Mkdocs server, where a step-by-step process will be provided to you. To do this:
1. `poetry install`
2. `poetry run mkdocs serve`

## Features

- Django 5
- Works with Python 3.11
- Registration via django-allauth
- 12-Factor based settings via django-environ
- TailwindCSS & StimulusJS (Hotwire) - comes with Webpack configure for dev & prod.
- Comes with custom user model ready to go
- Will work with any DB of your choosing, as long as it is supported by django
- Comes with docker-compose and makefile for rapid local development
- Media storage with any S3 compatible service. I use Minio both locally and in prod
- Structlog for logging setup both for local (console) and prod (json)
- Deployment to Caprover via Github Actions
- Messages handling
- Sitemaps enabled
- Sentry integration
- OpenTelemetry for tracing (Signoz in this case)
- Boilerplate for the Github Auth
- Testing with pytest
- Pre-commit

## Roadmap
- Add more default styling
- Create a core app and start populating it with CRUD operations
- Add optional Stripe support
- Add some tech overview to the Readme
- Add Wagtail for the blog
- Send emails via Anymail (Mailgun by default) (plus add Mailhog)
- Add github workflows to automate deployment (digitalocean, fly, appliku)
- Add pre-commit
- Add Sentry option
