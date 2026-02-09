import pytest
from django.contrib.auth import get_user_model

from core.choices import ProfileStates
from core.models import Profile


@pytest.mark.django_db
def test_user_save_does_not_revert_profile_state(sync_state_transitions):
    user_model = get_user_model()
    user = user_model.objects.create_user(
        username="signaluser",
        email="signaluser@example.com",
        password="password123",
    )
    profile = user.profile

    Profile.objects.filter(id=profile.id).update(state=ProfileStates.STRANGER)

    cached_user = user_model.objects.select_related("profile").get(id=user.id)

    Profile.objects.filter(id=profile.id).update(state=ProfileStates.SIGNED_UP)

    cached_user.save()

    profile.refresh_from_db()
    assert profile.state == ProfileStates.SIGNED_UP