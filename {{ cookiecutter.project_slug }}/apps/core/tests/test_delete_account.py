import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse


@pytest.mark.django_db
def test_delete_account_requires_confirmation(auth_client, user):
    url = reverse("delete_account")

    response = auth_client.post(url, data={"confirmation": "nope"})
    assert response.status_code == 302

    # user should still exist
    assert get_user_model().objects.filter(id=user.id).exists()


@pytest.mark.django_db
def test_delete_account_deletes_user(auth_client, user):
    url = reverse("delete_account")

    response = auth_client.post(url, data={"confirmation": "DELETE"})

    assert response.status_code == 302
    assert response["Location"].startswith(reverse("landing"))

    assert not get_user_model().objects.filter(id=user.id).exists()
