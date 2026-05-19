# django-saas-starter

A production-ready Cookiecutter template for building Django SaaS apps fast.

- **Stack:** Django 6.0.5 + Python 3.14.5 + Tailwind + Stimulus
- **Pragmatic defaults:** auth, payments (optional), email, API, landing pages, blog/docs (optional)
- **Deployment-ready:** Docker Compose (local + prod) + GitHub Actions (CapRover)

## Quickstart

```bash
cookiecutter git@github.com:rasulkireev/django-saas-starter.git
```

Then follow the generated project’s `README.md` for local development + deployment.

Important: in generated projects, run `uv run python manage.py makemigrations` (without app labels) before feature work so all app model changes are captured.

## What you get (high level)

### Core
- ✅ Django 6.0.5
- ✅ Python 3.14.5
- ✅ Environment variables via **django-environ**

### Auth
- ✅ User auth via **django-allauth**
- ❓ Social auth via **django-allauth**
  - ❓ Google (preconfigured)
  - ❓ GitHub (preconfigured)

### Frontend
- ✅ **Node.js 24.15.0 LTS** for frontend builds
- ✅ **Tailwind CSS** for styling
- ✅ **StimulusJS** for interactivity
- ✅ **Webpack** setup (assets pipeline)
- ✅ SEO-friendly templates (meta tags, JSON-LD schema, OG images)
- ✅ Root `DESIGN.md` based on Google Labs Code's DESIGN.md format for tool-neutral human/AI design guidance

### Pages & content
- ✅ Landing + pricing + auth pages + sitemap
- ✅ Feedback widget
- ❓ User-facing blog (app + templates)
- ❓ User-facing docs (app + templates)

### API
- ✅ API foundation via **django-ninja**
- ✅ Auth modes included (session, token, superuser)

### Database & storage
- ✅ Postgres 18 Docker images preconfigured
- ✅ Redis 8.6.3 Docker image preconfigured
- ✅ `pgvector` enabled
- ✅ `pg_stat_statements` enabled
- ❓ S3-compatible media storage (includes Minio for local + prod)

### Email & communication
- ✅ Email via **Anymail** + **Mailgun** (Mailhog for local)
- ✅ Styled UI message component
- ❓ MJML for email templating
- ❓ Buttondown for newsletters

### Dev experience
- ✅ Python dependency management with **uv** and a generated `uv.lock`
- ✅ Docker Compose (local + prod)
- ✅ Makefile helpers
- ✅ pytest
- ✅ Pre-commit: ruff + djlint
- ✅ Automated deploy to **CapRover** via **GitHub Actions**
- ❓ Optional CI workflow (runs Django checks + pytest on PRs)

### Observability & analytics
- ✅ Structlog (console in dev, JSON in prod)
- ❓ Sentry
- ❓ Logfire
- ❓ Healthcheck endpoint
- ❓ Posthog

### AI
- ✅ Tool-neutral `DESIGN.md` design source of truth for humans and AI coding agents
- ✅ Cursor Rules
- ❓ `pydanticai` for agents in-app

## Philosophy

This template aims to be:
- **Boring to maintain** (standard Django patterns, explicit config)
- **Fast to ship** (common SaaS pieces already wired)
- **Easy to extend** (clear app boundaries and sensible defaults)

## Contributing

Issues and PRs are welcome. If you’re proposing a bigger change, open an issue first so we can align on scope.

### Running template tests

This repo includes pytest-based tests that generate a project via Cookiecutter and assert the expected files are present/removed for various options.

```bash
uv run --group test pytest
```
