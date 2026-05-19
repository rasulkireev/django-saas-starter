#!/usr/bin/env python
"""Post-generation hook for cookiecutter-django-saas-starter."""

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


UV_VERSION = "0.11.15"
UV_MIN_VERSION = tuple(int(part) for part in UV_VERSION.split("."))


def remove_blog_app():
    """Remove blog app if generate_blog is 'n'."""
    blog_app_path = Path("apps/blog")
    if blog_app_path.exists():
        shutil.rmtree(blog_app_path)
        print("Removed blog app directory")


def remove_blog_templates():
    """Remove blog templates if generate_blog is 'n'."""
    blog_templates_path = Path("frontend/templates/blog")
    if blog_templates_path.exists():
        shutil.rmtree(blog_templates_path)
        print("Removed blog templates directory")


def remove_docs_app():
    """Remove docs app if generate_docs is 'n'."""
    docs_app_path = Path("apps/docs")
    if docs_app_path.exists():
        shutil.rmtree(docs_app_path)
        print("Removed docs app directory")


def remove_docs_templates():
    """Remove docs templates if generate_docs is 'n'."""
    docs_templates_path = Path("frontend/templates/docs")
    if docs_templates_path.exists():
        shutil.rmtree(docs_templates_path)
        print("Removed docs templates directory")


def remove_stripe_files():
    """Remove Stripe-related files if use_stripe is 'n'."""
    stripe_webhooks_path = Path("apps/core/stripe_webhooks.py")
    if stripe_webhooks_path.exists():
        stripe_webhooks_path.unlink()
        print("Removed Stripe webhooks module")

    stripe_tests_path = Path("apps/core/tests/test_stripe_webhooks.py")
    if stripe_tests_path.exists():
        stripe_tests_path.unlink()
        print("Removed Stripe webhook tests")

    pricing_template_path = Path("frontend/templates/pages/pricing.html")
    if pricing_template_path.exists():
        pricing_template_path.unlink()
        print("Removed pricing template")


def remove_chatwoot_files():
    """Remove Chatwoot-related files if use_chatwoot is 'n'."""
    chatwoot_template_path = Path("frontend/templates/components/chatwoot.html")
    if chatwoot_template_path.exists():
        chatwoot_template_path.unlink()
        print("Removed Chatwoot template")

    chatwoot_tests_path = Path("apps/core/tests/test_chatwoot_context.py")
    if chatwoot_tests_path.exists():
        chatwoot_tests_path.unlink()
        print("Removed Chatwoot context tests")

    chatwoot_docs_path = Path("apps/docs/content/deployment/chatwoot.md")
    if chatwoot_docs_path.exists():
        chatwoot_docs_path.unlink()
        print("Removed Chatwoot deployment guide")


def remove_mcp_files():
    """Remove MCP-related files if use_mcp is 'n'."""
    mcp_app_path = Path("apps/mcp_server")
    if mcp_app_path.exists():
        shutil.rmtree(mcp_app_path)
        print("Removed MCP server app")

    mcp_docs_path = Path("apps/docs/content/features/mcp.md")
    if mcp_docs_path.exists():
        mcp_docs_path.unlink()
        print("Removed MCP feature docs")


def remove_ci_workflow():
    """Remove CI workflow if use_ci is 'n'."""
    ci_workflow_path = Path(".github/workflows/ci.yml")
    if ci_workflow_path.exists():
        ci_workflow_path.unlink()
        print("Removed CI workflow")


def uv_version_tuple(version):
    """Parse uv's numeric version prefix into a comparable tuple."""
    match = re.match(r"^(\d+)\.(\d+)\.(\d+)", version)
    if match is None:
        return None

    return tuple(int(part) for part in match.groups())


def is_supported_uv_version(version):
    """Return whether an installed uv can generate a compatible lock file."""
    parsed_version = uv_version_tuple(version)
    if parsed_version is None:
        return False

    return parsed_version >= UV_MIN_VERSION


def valid_uv_command():
    """Return a working uv command if uv is already available."""
    uv_path = shutil.which("uv")
    if uv_path is None:
        return None

    try:
        completed = subprocess.run(
            [uv_path, "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None

    version_parts = completed.stdout.strip().split()
    if len(version_parts) < 2:
        return None

    installed_version = version_parts[1]
    if not is_supported_uv_version(installed_version):
        return None

    return [uv_path]


def run_quiet(command):
    """Run a command, surfacing output only to callers handling failures."""
    return subprocess.run(
        command,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
    )


def install_uv(temp_dir):
    """Install uv into a temporary virtual environment and return its path."""
    venv_path = Path(temp_dir) / "uv-bootstrap"
    subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)

    bin_dir = "Scripts" if os.name == "nt" else "bin"
    executable_suffix = ".exe" if os.name == "nt" else ""
    python_path = venv_path / bin_dir / ("python" + executable_suffix)
    uv_path = venv_path / bin_dir / ("uv" + executable_suffix)

    run_quiet(
        [str(python_path), "-m", "pip", "install", "--upgrade", "pip"],
    )
    run_quiet([str(python_path), "-m", "pip", "install", f"uv=={UV_VERSION}"])

    return [str(uv_path)]


def ensure_uv_command():
    """Return a compatible uv command, installing the minimum version if needed."""
    uv_command = valid_uv_command()
    if uv_command is not None:
        return uv_command, None

    print(
        f"uv {UV_VERSION} or newer not found; "
        "installing it temporarily for post-generation tasks..."
    )
    temp_dir = tempfile.TemporaryDirectory()
    try:
        return install_uv(temp_dir.name), temp_dir
    except (OSError, subprocess.CalledProcessError):
        temp_dir.cleanup()
        raise


def generate_uv_lock(uv_command):
    """Generate uv.lock so Docker and hosted deployments work immediately."""
    print("Generating uv.lock...")

    try:
        run_quiet([*uv_command, "lock"])
    except (OSError, subprocess.CalledProcessError) as exc:
        print("")
        print("WARNING: Could not generate uv.lock automatically.")
        print("Install uv and run `uv lock` before committing or deploying this project.")
        if isinstance(exc, subprocess.CalledProcessError) and exc.output:
            print("")
            print(exc.output)
        print(f"Original error: {exc}")
        return False

    print("Generated uv.lock")
    return True


def main():
    """Run post-generation tasks."""
    generate_blog = "{{ cookiecutter.generate_blog }}"
    generate_docs = "{{ cookiecutter.generate_docs }}"
    use_stripe = "{{ cookiecutter.use_stripe }}"
    use_chatwoot = "{{ cookiecutter.use_chatwoot }}"
    use_mcp = "{{ cookiecutter.use_mcp }}"
    use_ci = "{{ cookiecutter.use_ci }}"

    if generate_blog != "y":
        print("Blog generation disabled, removing blog-related files...")
        remove_blog_app()
        remove_blog_templates()
        print("Blog cleanup complete!")

    if generate_docs != "y":
        print("Docs generation disabled, removing docs-related files...")
        remove_docs_app()
        remove_docs_templates()
        print("Docs cleanup complete!")

    if use_stripe != "y":
        print("Stripe disabled, removing Stripe-related files...")
        remove_stripe_files()
        print("Stripe cleanup complete!")

    if use_chatwoot != "y":
        print("Chatwoot disabled, removing Chatwoot-related files...")
        remove_chatwoot_files()
        print("Chatwoot cleanup complete!")

    if use_mcp != "y":
        print("MCP disabled, removing MCP-related files...")
        remove_mcp_files()
        print("MCP cleanup complete!")

    if use_ci != "y":
        print("CI disabled, removing CI workflow...")
        remove_ci_workflow()
        print("CI cleanup complete!")

    uv_command = None
    uv_temp_dir = None
    try:
        uv_command, uv_temp_dir = ensure_uv_command()
    except (OSError, subprocess.CalledProcessError) as exc:
        print("")
        print("WARNING: Could not prepare uv for post-generation tasks.")
        print("Install uv and run `uv lock` before committing or deploying this project.")
        print(f"Original error: {exc}")

    try:
        if uv_command is not None:
            generate_uv_lock(uv_command)
    finally:
        if uv_temp_dir is not None:
            uv_temp_dir.cleanup()


if __name__ == "__main__":
    main()
