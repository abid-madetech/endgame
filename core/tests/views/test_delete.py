from uuid import uuid4

import pytest
from django.urls import reverse
from django.contrib.auth.models import User


@pytest.fixture
def user(db):
    return User.objects.create_user(username='user', password='pass')


@pytest.fixture
def authenticated_client(client, user):
    client.login(username='user', password='pass')
    return client

@pytest.mark.django_db
def test_delete_requires_auth(client):
    fake_id = str(uuid4())
    response = client.get(reverse('delete_ksb', args=[fake_id]))
    assert response.status_code == 302

@pytest.mark.django_db
def test_delete_ksb_successfully(authenticated_client, mocker):
    mock_delete = mocker.patch('core.views.requests.delete')
    mock_delete.return_value.status_code = 204

    fake_id = str(uuid4())
    response = authenticated_client.get(reverse('delete_ksb', args=[fake_id]))

    assert response.status_code == 302
    assert response.url == reverse('home')