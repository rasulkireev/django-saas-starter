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

    # optional apps on by default in this test helper
    assert (project_dir / "apps" / "blog").exists()
    assert (project_dir / "apps" / "docs").exists()

    # optional CI on by default
    assert (project_dir / ".github" / "workflows" / "ci.yml").exists()

    # sanity: package.json renders as valid JSON
    json.loads(_read_text(project_dir / "package.json"))


def test_generate_without_blog_removes_blog_app_and_templates(tmp_path: Path) -> None:
    project_dir = _generate(tmp_path, generate_blog="n")

    assert not (project_dir / "apps" / "blog").exists()
    assert not (project_dir / "frontend" / "templates" / "blog").exists()


def test_generate_without_docs_removes_docs_app_and_templates(tmp_path: Path) -> None:
    project_dir = _generate(tmp_path, generate_docs="n")

    assert not (project_dir / "apps" / "docs").exists()
    assert not (project_dir / "frontend" / "templates" / "docs").exists()


def test_generate_without_stripe_removes_stripe_files(tmp_path: Path) -> None:
    project_dir = _generate(tmp_path, use_stripe="n")

    assert not (project_dir / "apps" / "core" / "stripe_webhooks.py").exists()
    assert not (project_dir / "apps" / "core" / "tests" / "test_stripe_webhooks.py").exists()

    # pricing route should be removed when stripe is off
    urls_py = project_dir / "apps" / "pages" / "urls.py"
    assert urls_py.exists()
    _assert_not_contains(urls_py, "pricing")


def test_generate_with_stripe_keeps_stripe_files_and_pricing(tmp_path: Path) -> None:
    project_dir = _generate(tmp_path, use_stripe="y")

    assert (project_dir / "apps" / "core" / "stripe_webhooks.py").exists()
    assert (project_dir / "apps" / "core" / "tests" / "test_stripe_webhooks.py").exists()
    urls_py = project_dir / "apps" / "pages" / "urls.py"
    assert urls_py.exists()
    _assert_contains(urls_py, "pricing")


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


def test_use_posthog_toggles_posthog_snippet(tmp_path: Path) -> None:
    enabled = _generate(tmp_path, use_posthog="y")
    disabled = _generate(tmp_path, use_posthog="n")

    enabled_base = enabled / "frontend" / "templates" / "base_landing.html"
    disabled_base = disabled / "frontend" / "templates" / "base_landing.html"

    _assert_contains(enabled_base, "posthog.init")
    _assert_not_contains(disabled_base, "posthog.init")


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
