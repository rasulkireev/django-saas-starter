from __future__ import annotations

from pathlib import Path

from cookiecutter.main import cookiecutter


def _generate(tmp_path: Path, **extra_context: str) -> Path:
    """Generate a project into tmp_path and return the generated project dir."""
    # Keep context minimal but explicit so tests fail loudly if prompts/keys change.
    context = {
        "project_name": "Test Project",
        "repo_url": "https://example.com/test/test-project",
        "project_description": "Test Project Description",
        "author_name": "Ada Lovelace",
        "author_email": "ada@example.com",
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

    out_dir = cookiecutter(
        str(template_dir),
        no_input=True,
        extra_context=context,
        output_dir=str(tmp_path),
    )
    return Path(out_dir)


def test_generate_default_structure(tmp_path: Path) -> None:
    project_dir = _generate(tmp_path)

    assert project_dir.exists()
    assert (project_dir / "manage.py").exists()

    # apps present by default
    assert (project_dir / "apps" / "core").exists()
    assert (project_dir / "apps" / "pages").exists()

    # optional apps on by default in this test helper
    assert (project_dir / "apps" / "blog").exists()
    assert (project_dir / "apps" / "docs").exists()

    # optional CI on by default
    assert (project_dir / ".github" / "workflows" / "ci.yml").exists()


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


def test_generate_without_ci_removes_ci_workflow(tmp_path: Path) -> None:
    project_dir = _generate(tmp_path, use_ci="n")

    assert not (project_dir / ".github" / "workflows" / "ci.yml").exists()
