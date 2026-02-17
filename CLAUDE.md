# CLAUDE.md

This file is for AI coding agents (Claude, Codex, etc.) working on **this repository** and on projects generated from this template.

## What this repo is

`django-saas-starter` is a **Cookiecutter template repository**.

- Most source files live under: `{{ cookiecutter.project_slug }}/...`
- Any file containing `{{ ... }}` / `{% ... %}` is a template and must render correctly for all supported option combinations.
- When changing template code, prefer verifying by **generating a fresh project** and running its tests.

## High-level architecture (generated project)

Typical generated layout:

- `apps/` — Django apps (API, core, pages, etc.)
- `config/` or `settings/` — project settings / environment configuration
- `templates/` — server-rendered HTML templates
- `static/` — static assets (Tailwind/JS build output varies by options)
- `deployment/` — deployment entrypoint / Docker-related files

Common concerns:

- Auth: django-allauth
- Payments (optional): Stripe integration
- API: Django Ninja endpoints

## Quick commands (this template repo)

### Lint / format

If this repo uses `pre-commit` (recommended):

```bash
pre-commit run -a
```

### Run tests (if present)

```bash
pytest
```

> Note: Cookiecutter template repos often need specialized tests that generate a project and then run that project’s checks.

## Verify template changes (recommended workflow)

1) Generate a project into a temp directory:

```bash
cookiecutter . --no-input -o /tmp
# or interactively
cookiecutter . -o /tmp
```

2) Enter the generated project and run the standard Django checks/tests:

```bash
cd /tmp/<generated-project-slug>
python manage.py check
python manage.py test
```

3) If the generated project uses `uv` (common in this repo), install + run via `uv`:

```bash
uv sync
uv run python manage.py test
```

## Templating guidelines (important)

- **Never** introduce trailing commas / missing commas in `package.json`-like templates.
- Keep conditionals minimal; prefer generating valid files for all option paths.
- When adding new files, consider whether they belong to:
  - the template repo root (maintainer docs like this file), or
  - the generated project (`{{ cookiecutter.project_slug }}/...`).

## How to add a CHANGELOG entry

Update `CHANGELOG.md` under `[Unreleased]` with a short bullet describing the change.
