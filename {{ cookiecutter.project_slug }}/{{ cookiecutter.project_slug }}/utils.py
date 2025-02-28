import structlog


def get_{{ cookiecutter.project_slug }}_logger(name):
    """This will add a `{{ cookiecutter.project_slug }}` prefix to logger for easy configuration."""

    return structlog.get_logger(
        f"{{ cookiecutter.project_slug }}.{name}",
        project="{{ cookiecutter.project_slug }}"
    )
