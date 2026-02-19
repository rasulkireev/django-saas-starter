import pytest
from django.conf import settings

from apps.core import tasks as core_tasks


def pytest_configure(config):
    settings.STORAGES["staticfiles"]["BACKEND"] = (
        "django.contrib.staticfiles.storage.StaticFilesStorage"
    )


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username="testuser",
        email="testuser@example.com",
        password="password123",
    )


@pytest.fixture
def auth_client(client, user):
    client.force_login(user)
    return client


@pytest.fixture
def profile(user):
    return user.profile


@pytest.fixture
def sync_state_transitions(monkeypatch):
    """Run queued state-transition tracking synchronously inside tests."""

    def _fake_async_task(func_path, *args, **kwargs):
        if func_path == "apps.core.tasks.track_state_change":
            kwargs.pop("group", None)
            return core_tasks.track_state_change(*args, **kwargs)
        return None

    monkeypatch.setattr("apps.core.models.async_task", _fake_async_task)
    return _fake_async_task
