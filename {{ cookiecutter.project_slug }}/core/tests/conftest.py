import pytest
from django.conf import settings
from django.core.management import call_command
from django.contrib.auth import get_user_model

User = get_user_model()


def pytest_configure(config):
    settings.STORAGES['staticfiles']['BACKEND'] = (
        'django.contrib.staticfiles.storage.StaticFilesStorage'
    )


@pytest.fixture
def user(db):
    """Create a test user"""
    return User.objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password='testpass123'
    )
