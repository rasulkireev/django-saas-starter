from __future__ import annotations

import json
import uuid
from pathlib import Path

import pytest
from cookiecutter.main import cookiecutter


def _generate(tmp_path: Path, **extra_context: str) -> Path:
    """Generate a project into tmp_path and return the generated project dir."""
    # Keep context explicit so tests fail loudly if prompts/keys change.
    context: dict[str, str] = {
        "project_name": "Test Project",
        "repo_url": "https://example.com/test/test-project",
        "project_description": "Test Project Description",
        "author_name": "Ada Lovelace",
        "author_email": "ada@example.com",
        "author_url": "",
        "project_main_color": "green",
        # defaults (can be overridden per test)
        "use_posthog": "n",
        "use_buttondown": "n",
        "use_s3": "n",
        "use_stripe": "n",
        "use_sentry": "n",
        "generate_blog": "y",
        "generate_docs": "y",
        "use_mjml": "n",
        "use_ai": "n",
        "use_logfire": "n",
        "use_healthchecks": "n",
        "use_ci": "y",
    }
    context.update(extra_context)

    template_dir = Path(__file__).resolve().parents[1]

    output_dir = tmp_path / uuid.uuid4().hex
    output_dir.mkdir(parents=True, exist_ok=True)

    out_dir = cookiecutter(
        str(template_dir),
        no_input=True,
        extra_context=context,
        output_dir=str(output_dir),
    )
    return Path(out_dir)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _assert_contains(path: Path, needle: str) -> None:
    content = _read_text(path)
    assert needle in content, f"Expected to find {needle!r} in {path}"


def _assert_not_contains(path: Path, needle: str) -> None:
    content = _read_text(path)
    assert needle not in content, f"Expected not to find {needle!r} in {path}"


def test_generate_default_structure(tmp_path: Path) -> None:
    project_dir = _generate(tmp_path)

    assert project_dir.exists()
    assert project_dir.name == "test_project"

    # sanity: core entrypoints exist
    assert (project_dir / "manage.py").exists()
    assert (project_dir / "pyproject.toml").exists()
    assert (project_dir / "frontend" / "templates").exists()

    # new feature: account deletion flow
    assert (project_dir / "apps" / "core" / "tests" / "test_delete_account.py").exists()
    _assert_contains(project_dir / "apps" / "core" / "urls.py", "delete-account")

    # apps present by default
    assert (project_dir / "apps" / "core").exists()
    assert (project_dir / "apps" / "pages").exists()

    # auth error styling should include dark-mode contrast classes
    _assert_contains(
        project_dir / "apps" / "core" / "utils.py",
        'dark:bg-red-950/40',
    )

    # transactional email hardening should ship in generated projects
    assert (project_dir / "apps" / "core" / "tests" / "test_email_delivery.py").exists()
    _assert_contains(
        project_dir / "apps" / "core" / "utils.py",
        'def send_transactional_email(',
    )

    # optional apps on by default in this test helper
    assert (project_dir / "apps" / "blog").exists()
    assert (project_dir / "apps" / "docs").exists()
    assert not (
        Path(__file__).resolve().parents[1]
        / "{{ cookiecutter.project_slug }}"
        / "apps"
        / "core"
        / "migrations"
        / "0002_initial.py"
    ).exists()
    assert (project_dir / "apps" / "core" / "migrations" / "0002_initial.py").exists()
    assert (project_dir / "apps" / "pages" / "migrations" / "0001_initial.py").exists()
    assert (project_dir / "apps" / "blog" / "migrations" / "0001_initial.py").exists()

    _assert_contains(project_dir / "deployment" / "entrypoint.sh", "wait_for_database")
    _assert_contains(project_dir / "deployment" / "entrypoint.sh", "exec gunicorn")
    _assert_contains(project_dir / "deployment" / "Dockerfile.server", "chmod +x deployment/entrypoint.sh")
    _assert_contains(project_dir / "deployment" / "Dockerfile.server", '["sh", "deployment/entrypoint.sh", "-s"]')
    _assert_contains(
        Path(__file__).resolve().parents[1] / "hooks" / "post_gen_project.py",
        "Generating fresh initial migrations",
    )

    # optional CI on by default
    assert (project_dir / ".github" / "workflows" / "ci.yml").exists()

    # sanity: package.json renders as valid JSON
    json.loads(_read_text(project_dir / "package.json"))


def test_default_generation_includes_passkey_auth(tmp_path: Path) -> None:
    project_dir = _generate(tmp_path)

    settings_py = project_dir / "test_project" / "settings.py"
    urls_py = project_dir / "test_project" / "urls.py"
    views_py = project_dir / "apps" / "pages" / "views.py"

    _assert_contains(project_dir / "pyproject.toml", "fido2>=2.2.0,<3")
    _assert_contains(settings_py, '"allauth.mfa"')
    _assert_contains(settings_py, 'ACCOUNT_LOGIN_METHODS = {"email"}')
    _assert_contains(settings_py, 'ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*"]')
    _assert_contains(settings_py, 'ACCOUNT_EMAIL_VERIFICATION = "optional"')
    _assert_contains(settings_py, "ACCOUNT_EMAIL_VERIFICATION_BY_CODE_ENABLED = False")
    _assert_contains(settings_py, "EMAIL_DELIVERY_RETRY_BACKOFF_SECONDS = (0.0, 1.0, 3.0)")
    _assert_contains(settings_py, 'SITE_HOST = SITE_URL.replace("http://", "").replace("https://", "").split("/")[0].split(":")[0]')
    _assert_contains(settings_py, 'ALLOWED_HOSTS = [SITE_HOST]')
    _assert_contains(settings_py, 'ALLOWED_HOSTS = ["*"]')
    _assert_contains(settings_py, '"http://localhost:8000"')
    _assert_contains(settings_py, '"http://127.0.0.1:8000"')
    _assert_contains(settings_py, '"http://backend:8000"')
    _assert_contains(settings_py, '"https://*.ngrok-free.app"')
    _assert_contains(settings_py, '"https://*.ngrok.app"')
    _assert_contains(settings_py, '"https://*.trycloudflare.com"')
    _assert_contains(settings_py, '"https://*.loca.lt"')
    _assert_contains(settings_py, "MFA_PASSKEY_LOGIN_ENABLED = True")
    _assert_contains(settings_py, "MFA_PASSKEY_SIGNUP_ENABLED = False")
    _assert_contains(settings_py, "MFA_WEBAUTHN_ALLOW_INSECURE_ORIGIN = DEBUG")
    _assert_contains(settings_py, 'ALLOW_SIGNUPS = env.bool("ALLOW_SIGNUPS", default=True)')

    _assert_contains(project_dir / ".env.example", "ALLOW_SIGNUPS=True")
    _assert_contains(project_dir / ".env.example", "MAILGUN_SENDER_DOMAIN=mg.test_project.app")
    _assert_contains(settings_py, 'env("MAILGUN_SENDER_DOMAIN", default="mg.test_project.app")')
    _assert_contains(
        project_dir / "apps" / "docs" / "content" / "deployment" / "environment-variables.md",
        "**ALLOW_SIGNUPS**",
    )
    _assert_contains(
        project_dir / "frontend" / "templates" / "account" / "signup_closed.html",
        "Signups paused",
    )
    _assert_contains(
        project_dir / "apps" / "core" / "tests" / "test_signup_gating.py",
        "test_account_signup_adapter_can_pause_new_signups",
    )

    _assert_contains(urls_py, "accounts/signup/passkey/")
    _assert_contains(urls_py, "account_signup_by_passkey")
    _assert_contains(views_py, "AccountSignupByPasskeyView")

    _assert_contains(
        project_dir / "frontend" / "templates" / "account" / "login.html",
        "Sign in with a passkey",
    )
    _assert_contains(
        project_dir
        / "frontend"
        / "templates"
        / "mfa"
        / "webauthn"
        / "snippets"
        / "login_script.html",
        "window.webauthnJSON.get(requestOptions)",
    )
    _assert_not_contains(
        project_dir / "frontend" / "templates" / "account" / "signup.html",
        "Sign up using a passkey",
    )
    _assert_contains(
        project_dir / "frontend" / "templates" / "pages" / "user-settings.html",
        "Add passkey",
    )
    _assert_contains(
        project_dir / "frontend" / "templates" / "mfa" / "index.html",
        "Passkeys",
    )
    _assert_contains(
        project_dir / "frontend" / "templates" / "account" / "email.html",
        "Email addresses",
    )


def test_generated_mfa_templates_use_configured_project_colour(tmp_path: Path) -> None:
    project_dir = _generate(tmp_path, project_main_color="purple")

    _assert_contains(
        project_dir / "frontend" / "templates" / "mfa" / "webauthn" / "add_form.html",
        "bg-purple-600",
    )
    _assert_contains(
        project_dir / "frontend" / "templates" / "account" / "email.html",
        "focus:ring-purple-500",
    )
    _assert_not_contains(
        project_dir / "frontend" / "templates" / "mfa" / "webauthn" / "add_form.html",
        "green-",
    )


def test_generate_without_blog_removes_blog_app_and_templates(tmp_path: Path) -> None:
    project_dir = _generate(tmp_path, generate_blog="n")

    assert not (project_dir / "apps" / "blog").exists()
    assert not (project_dir / "frontend" / "templates" / "blog").exists()


def test_generate_with_blog_includes_admin_blog_crud_api(tmp_path):
    project_dir = _generate(tmp_path, generate_blog="y")

    api_views = project_dir / "apps" / "api" / "views.py"
    api_schemas = project_dir / "apps" / "api" / "schemas.py"
    api_tests = project_dir / "apps" / "api" / "tests.py"

    for endpoint in [
        '"/blog-posts/submit"',
        '"/internal/blog-posts"',
        '"/internal/blog-posts/{blog_post_id}"',
        '"/internal/blog-posts/{blog_post_id}/review"',
        '"/internal/blog-posts/{blog_post_id}/publish"',
    ]:
        _assert_contains(api_views, endpoint)

    for method in ["@api.post", "@api.get", "@api.put", "@api.patch", "@api.delete"]:
        _assert_contains(api_views, method)

    _assert_contains(api_views, "auth=[superuser_api_auth]")
    _assert_contains(api_schemas, "class BlogPostIn")
    _assert_contains(api_schemas, "class BlogPostUpdateIn")
    _assert_contains(api_tests, "class BlogPostApiTests")
    _assert_contains(api_tests, "test_delete_internal_blog_post_deletes_existing_post")


def test_generate_without_blog_removes_admin_blog_crud_api(tmp_path):
    project_dir = _generate(tmp_path, generate_blog="n")

    api_views = project_dir / "apps" / "api" / "views.py"
    api_schemas = project_dir / "apps" / "api" / "schemas.py"

    _assert_not_contains(api_views, "BlogPost")
    _assert_not_contains(api_views, "/internal/blog-posts")
    _assert_not_contains(api_schemas, "BlogPostIn")


def test_generate_without_docs_removes_docs_app_and_templates(tmp_path: Path) -> None:
    project_dir = _generate(tmp_path, generate_docs="n")

    assert not (project_dir / "apps" / "docs").exists()
    assert not (project_dir / "frontend" / "templates" / "docs").exists()


def test_generate_without_stripe_removes_stripe_files(tmp_path: Path) -> None:
    project_dir = _generate(tmp_path, use_stripe="n")

    assert not (project_dir / "apps" / "core" / "stripe_webhooks.py").exists()
    assert not (project_dir / "apps" / "core" / "tests" / "test_stripe_webhooks.py").exists()
    assert not (project_dir / "frontend" / "templates" / "pages" / "pricing.html").exists()

    # pricing route should be removed when stripe is off
    urls_py = project_dir / "apps" / "pages" / "urls.py"
    assert urls_py.exists()
    _assert_not_contains(urls_py, "pricing")

    # no subscription-only helpers or API fields should leak into the generated project
    _assert_not_contains(project_dir / "apps" / "core" / "models.py", "has_active_subscription")
    _assert_not_contains(project_dir / "apps" / "api" / "schemas.py", "has_pro_subscription")
    _assert_not_contains(project_dir / "apps" / "api" / "views.py", "has_pro_subscription")

    choices_py = project_dir / "apps" / "core" / "choices.py"
    _assert_not_contains(choices_py, "TRIAL_STARTED")
    _assert_not_contains(choices_py, "TRIAL_ENDED")
    _assert_not_contains(choices_py, "SUBSCRIBED")
    _assert_not_contains(choices_py, "CANCELLED")
    _assert_not_contains(choices_py, "CHURNED")

    landing_page = project_dir / "frontend" / "templates" / "pages" / "landing-page.html"
    _assert_not_contains(landing_page, "How does pricing work?")
    _assert_not_contains(landing_page, "premium plans")

    privacy_policy = project_dir / "frontend" / "templates" / "pages" / "privacy-policy.html"
    _assert_not_contains(privacy_policy, "processed securely through Stripe")
    _assert_not_contains(privacy_policy, "Process transactions and send related information")
    _assert_not_contains(privacy_policy, "Secure payment processing through PCI-compliant providers (Stripe)")
    _assert_not_contains(privacy_policy, "Stripe (payment processing)")
    _assert_not_contains(privacy_policy, "Payment records: Retained for 7 years for tax and accounting purposes")

    terms_of_service = project_dir / "frontend" / "templates" / "pages" / "terms-of-service.html"
    _assert_not_contains(terms_of_service, "Paid subscriptions are billed in advance on a recurring basis.")
    _assert_not_contains(terms_of_service, "subscription tier")
    _assert_contains(terms_of_service, "The default starter does not include recurring paid subscriptions.")


def test_generate_with_stripe_keeps_stripe_files_and_pricing(tmp_path: Path) -> None:
    project_dir = _generate(tmp_path, use_stripe="y")

    assert (project_dir / "apps" / "core" / "stripe_webhooks.py").exists()
    assert (project_dir / "apps" / "core" / "tests" / "test_stripe_webhooks.py").exists()
    assert (project_dir / "frontend" / "templates" / "pages" / "pricing.html").exists()
    urls_py = project_dir / "apps" / "pages" / "urls.py"
    assert urls_py.exists()
    _assert_contains(urls_py, "pricing")
    _assert_contains(project_dir / "apps" / "api" / "schemas.py", "has_pro_subscription")
    _assert_contains(project_dir / "apps" / "core" / "models.py", "has_active_subscription")


def test_generate_without_ci_removes_ci_workflow(tmp_path: Path) -> None:
    project_dir = _generate(tmp_path, use_ci="n")

    assert not (project_dir / ".github" / "workflows" / "ci.yml").exists()


@pytest.mark.parametrize(
    ("flag", "dep"),
    [
        ("use_mjml", "django-mjml"),
        ("use_ai", "pydantic-ai"),
        ("use_ai", "pgvector"),
        ("use_logfire", "logfire"),
        ("use_posthog", "posthog"),
        ("use_sentry", "sentry-sdk"),
    ],
)
def test_optional_dependencies_are_toggled_in_pyproject(tmp_path: Path, flag: str, dep: str) -> None:
    enabled = _generate(tmp_path, **{flag: "y"})
    disabled = _generate(tmp_path, **{flag: "n"})

    enabled_pyproject = _read_text(enabled / "pyproject.toml")
    disabled_pyproject = _read_text(disabled / "pyproject.toml")

    assert dep in enabled_pyproject
    assert dep not in disabled_pyproject


def test_use_s3_toggles_minio_in_docker_compose(tmp_path: Path) -> None:
    enabled = _generate(tmp_path, use_s3="y")
    disabled = _generate(tmp_path, use_s3="n")

    enabled_compose = _read_text(enabled / "docker-compose-local.yml")
    disabled_compose = _read_text(disabled / "docker-compose-local.yml")

    assert "minio" in enabled_compose.lower()
    assert "minio" not in disabled_compose.lower()


def test_local_compose_waits_for_frontend_ready_and_uses_supported_node(tmp_path: Path) -> None:
    project_dir = _generate(tmp_path)

    compose = _read_text(project_dir / "docker-compose-local.yml")
    styles = _read_text(project_dir / "frontend" / "src" / "styles" / "index.css")

    assert "image: node:24" in compose
    assert 'condition: service_healthy' in compose
    assert 'test -f /app/frontend/build/manifest.json' in compose
    assert styles.index('@import "tailwindcss";') < styles.index('@import "./pygments.css";') < styles.index('@config "../../../tailwind.config.js";')


def test_use_posthog_toggles_posthog_snippet(tmp_path: Path) -> None:
    enabled = _generate(tmp_path, use_posthog="y")
    disabled = _generate(tmp_path, use_posthog="n")

    enabled_base = enabled / "frontend" / "templates" / "base_landing.html"
    disabled_base = disabled / "frontend" / "templates" / "base_landing.html"

    _assert_contains(enabled_base, "posthog.init")
    _assert_not_contains(disabled_base, "posthog.init")


def test_use_sentry_includes_observability_defaults(tmp_path: Path) -> None:
    project_dir = _generate(tmp_path, use_sentry="y")

    settings_py = project_dir / "test_project" / "settings.py"
    env_example = project_dir / ".env.example"
    docs = project_dir / "apps" / "docs" / "content" / "deployment" / "environment-variables.md"

    _assert_contains(settings_py, "SENTRY_RELEASE = env(")
    _assert_contains(settings_py, "SENTRY_TRACES_SAMPLE_RATE = env.float(")
    _assert_contains(settings_py, "SENTRY_PROFILE_SESSION_SAMPLE_RATE = env.float(")
    _assert_contains(settings_py, "SENTRY_ENABLE_LOGS = env.bool(")
    _assert_contains(settings_py, "SENTRY_SEND_DEFAULT_PII = env.bool(")
    _assert_contains(settings_py, "SENTRY_INCLUDE_LOCAL_VARIABLES = env.bool(")
    _assert_contains(settings_py, "SENTRY_MAX_BREADCRUMBS = env.int(")
    _assert_contains(settings_py, "release=SENTRY_RELEASE or None")
    _assert_contains(settings_py, "enable_logs=SENTRY_ENABLE_LOGS")
    _assert_contains(settings_py, "CustomLoggingIntegration(level=logging.INFO, event_level=logging.ERROR)")
    _assert_contains(settings_py, "before_send=before_send")

    for key in [
        "SENTRY_RELEASE=",
        "SENTRY_TRACES_SAMPLE_RATE=1.0",
        "SENTRY_PROFILE_SESSION_SAMPLE_RATE=1.0",
        "SENTRY_ENABLE_LOGS=True",
        "SENTRY_SEND_DEFAULT_PII=False",
        "SENTRY_INCLUDE_LOCAL_VARIABLES=False",
        "SENTRY_MAX_BREADCRUMBS=100",
    ]:
        _assert_contains(env_example, key)
        _assert_contains(docs, key.split("=")[0])


def test_generated_project_does_not_contain_unrendered_cookiecutter_vars(tmp_path: Path) -> None:
    project_dir = _generate(tmp_path)

    base_app = project_dir / "frontend" / "templates" / "base_app.html"
    base_landing = project_dir / "frontend" / "templates" / "base_landing.html"

    _assert_not_contains(base_app, "rasulkireev.com")
    _assert_not_contains(base_landing, "rasulkireev.com")

    # When author_url is empty, it should not be rendered into JSON-LD as an empty string.
    _assert_not_contains(base_app, '"url": ""')
    _assert_not_contains(base_landing, '"url": ""')

    # Some frontend templates intentionally embed Cookiecutter variables inside Django-template
    # string literals (so they are not evaluated by Cookiecutter). We keep this test as a
    # coarse regression check, but exclude those known files.
    allowlist = {
        Path("frontend/templates/pages/user-settings.html"),
        Path("frontend/templates/docs/base_docs.html"),
    }

    offenders: list[str] = []
    for path in project_dir.rglob("*"):
        if not path.is_file():
            continue

        rel = path.relative_to(project_dir)
        if rel.parts[0] == ".venv":
            continue
        if rel in allowlist:
            continue

        # Skip binary-ish files
        if path.suffix in {".png", ".jpg", ".jpeg", ".gif", ".ico", ".woff", ".woff2"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        if "{{ cookiecutter." in text:
            offenders.append(str(rel))

    assert offenders == [], f"Unrendered cookiecutter vars found in: {offenders}"


def test_generated_project_does_not_contain_template_author_leaks(tmp_path: Path) -> None:
    project_dir = _generate(tmp_path)

    banned_literals = ("rasulkireev.com", "Rasul")
    offenders: list[str] = []

    for path in project_dir.rglob("*"):
        if not path.is_file():
            continue
        if path.relative_to(project_dir).parts[0] == ".venv":
            continue
        if path.suffix in {".png", ".jpg", ".jpeg", ".gif", ".ico", ".woff", ".woff2"}:
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        if any(token in text for token in banned_literals):
            offenders.append(str(path.relative_to(project_dir)))

    assert offenders == [], f"Hard-coded template author literals found in: {offenders}"
