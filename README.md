To start you'll need to start the Mkdocs server, where a step-by-step process will be provided to you. To do this:
1. `poetry install`
2. `poetry run mkdocs serve`

## Features

Legend:
- ✅ Non-optional
- ❓ Optional

### Core
- ✅ Django 5
- ✅ Python 3.13
- ✅ Environment variables via **django-environ**

### Auth
- ✅ Regular User Auth via **django-allauth**
- ❓ Socail Auth via **django-allauth**:
  - ❓ **Google** pre configured
  - ❓ **Github** pre configured

### Communication
- ✅ **Anymail** for email sending with **Mailgun** (Mailhog for local)
- ✅ **Messages** handling with nice tempalte component pre-installed
- ✅ **MJML** for email templating
- ❓ **Buttondown** for newsletters

### Frontend
- ✅ **Webpack** pre-configured
- ✅ **TailwindCSS** for styling
- ✅ **StimulusJS** for interactivity via Webpack
- ✅ SEO optimized templates, pre-configured:
  - metatags
  - json-ld schema
  - OG images

### Database & Storage
- ✅ Any Django Supported db will work fine.
- ✅ Custom **Postgres** 18 db pre-configured in env files and docker compose.
- ✅ **pgvector** is installed both in Postgres and in the App
- ✅ **pg_stat_statements** is pre-installed on postgres too.
- ❓ Media storage with any **S3 compatible** service. Comes with **Minio** both locally and in prod.

### Dev Tools
- ✅ **Docker Compose** for **local dev** and **prod** pre-configured.
- ✅ **Makefile** is preconfigured for necessary commands.
- ✅ Automated Deployment to **Caprover** via **Github Actions** is pre-confuigured.
- ✅ Testing with **pytest**
- ✅ **Pre-commit** for code quality checks: **ruff**, **djlint**

### Logging & Monitoring
- ✅ Structlog for logging setup both for local (console) and prod (json)
- ❓ Sentry integration
- ❓ Logfire for prod and dev logging dashboards

### Pages
- ✅ landing, pricing, signin/signup, sitemap, blog, docs
- ✅ API support with django-ninja
- ✅ Way to collect feedback pre-installed via a nice widget

### API
- ✅ django-ninja for api endpoints
- ✅ 3 auth modes pre-installed (session, token, superuser)

### Payments
- ❓ Stripe for payments (subscriptions) via **djstripe**
