# AGENTS.md — django-saas-starter (Cookiecutter Template)

This repo is a **Cookiecutter template**, not a single Django app.
Your job is to change the template safely so generated projects stay valid across feature flags.

## 0) What success looks like

A good change here means:
1. Template renders successfully via Cookiecutter.
2. Optional flags (`use_stripe`, `generate_docs`, etc.) still behave correctly.
3. Generated project still passes its baseline checks.
4. Changelog/docs are updated when behavior changes.

---

## 1) Canonical workflow (agent-first)

Follow this exact order for any implementation task.

1. **Understand scope**
   - Read `README.md`, `cookiecutter.json`, and `tests/test_cookiecutter_template.py`.
   - If relevant, inspect `hooks/post_gen_project.py` and files under `{{ cookiecutter.project_slug }}/`.

2. **Create a branch**
   - Branch name format: `fix/<short-topic>` or `feat/<short-topic>`.

3. **Implement at template level**
   - Edit files inside `{{ cookiecutter.project_slug }}/...` (or root metadata/tests/hooks) as needed.
   - Keep Jinja templating valid (`{% if ... %}`, `{{ cookiecutter... }}`).

4. **Validate locally (required)**
   - Run template test suite:
     ```bash
     uv run --group test pytest
     ```
   - If your change affects generated-project runtime behavior, also do a quick render + smoke check (see command reference below).

5. **Update docs/changelog**
   - Add or adjust entries in `CHANGELOG.md` (`[Unreleased]`) for user-visible changes.
   - Update README when setup, behavior, options, or workflow changed.

6. **Commit + open PR**
   - Commit with clear message (`feat: ...` / `fix: ...`).
   - Push branch and open PR with:
     - what changed
     - why
     - validation output
     - flag combinations tested (if applicable)

---

## 2) Quick command reference

## Template repo (this repository)

```bash
# install/sync deps (first run)
uv sync --group test

# run template tests (required)
uv run --group test pytest

# run CI-equivalent locally (same as GitHub workflow)
uv run --group test pytest
```

## Smoke-test a generated project (when needed)

```bash
# generate project interactively
cookiecutter .

# OR non-interactive example
tmpdir=$(mktemp -d) && cookiecutter . --no-input -o "$tmpdir"
cd "$tmpdir"/*

# generated project checks
uv sync
uv run python manage.py check
uv run pytest -q
```

If frontend/build behavior is part of your change, also run in generated project:

```bash
npm install
npm run lint
```

---

## 3) Architecture conventions (where to change things)

All generated app code lives under `{{ cookiecutter.project_slug }}/`.

- `apps/core/` → shared domain logic, auth-adjacent flows, common models/views/forms/tasks.
- `apps/pages/` → landing + marketing pages (pricing, legal, static pages).
- `apps/api/` → Django Ninja API (schemas, auth, routers/views).
- `apps/blog/` → user-facing blog (optional via `generate_blog`).
- `apps/docs/` → user-facing docs (optional via `generate_docs`).
- `{{ cookiecutter.project_slug }}/settings.py` → env-driven config, installed apps, integrations.
- `{{ cookiecutter.project_slug }}/urls.py` → top-level URL wiring.
- `hooks/post_gen_project.py` → remove optional files after generation when flags are disabled.
- `tests/test_cookiecutter_template.py` → template-level regression tests (required to update with behavior changes).

Rule: prefer template tests that assert render-time behavior across enabled/disabled flags.

---

## 4) Guardrails for high-risk areas

## Migrations

- Put schema changes in the correct app under `apps/*/migrations/`.
- Keep generated migrations deterministic and import-clean.
- Do not hand-edit historical migrations unless explicitly required.
- Ensure optional-app toggles do not leave broken migration references.

## Auth

- Auth stack relies on `django-allauth`; keep URL/template flows consistent.
- When changing login/signup/password templates, verify dark/light styles and form error readability.
- Avoid hard-coded maintainer identity strings (author/site info must come from cookiecutter variables).

## Billing (Stripe)

- All Stripe behavior must be gated by `use_stripe`.
- If `use_stripe = n`, Stripe files/routes/tests must be absent (see existing tests).
- Webhook logic belongs in `apps/core/stripe_webhooks.py`; keep event handling idempotent and defensive.

## Docs/blog optionality

- `generate_docs` and `generate_blog` must fully remove corresponding app + templates when `n`.
- Any new docs/blog files must be covered by post-gen cleanup and tests.

---

## 5) PR checklist (copy into PR description)

- [ ] Scope is implemented in template files (not only in one rendered sample).
- [ ] `uv run --group test pytest` passes.
- [ ] Added/updated tests for new behavior or flag toggles.
- [ ] Changelog updated under `[Unreleased]` (if user-visible change).
- [ ] README/docs updated (if workflow/options changed).
- [ ] Optional flags still render valid projects for affected paths.
- [ ] No hard-coded maintainer-specific literals added.

---

## 6) Definition of Done (DoD)

A task is done only if:
1. Code + template logic are complete.
2. Template tests pass locally.
3. Relevant docs/changelog are updated.
4. PR is open with validation evidence.
5. No known regressions across related cookiecutter options.

---

## 7) Do NOT do (common footguns)

- Do **not** edit only a generated output and call it done.
- Do **not** break Jinja syntax inside JSON/YAML/TOML files.
- Do **not** add Stripe/docs/blog code without updating option toggles + tests.
- Do **not** introduce hard-coded personal/company identifiers into template output.
- Do **not** skip running template tests before opening PR.
- Do **not** remove CI/workflow expectations without explicit requirement.

Keep changes minimal, test-backed, and flag-aware.