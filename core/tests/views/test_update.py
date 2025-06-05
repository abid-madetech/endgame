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
def test_update_ksb_requires_auth(client):
    fake_id = str(uuid4())
    response = client.get(reverse('update_ksb', args=[fake_id]))
    assert response.status_code == 302


@pytest.mark.django_db
def test_authenticated_user_can_access_update_page(authenticated_client):
    fake_id = str(uuid4())
    response = authenticated_client.get(reverse('update_ksb', args=[fake_id]))
    assert response.status_code == 200
    assert 'Update KSB' in response.content.decode()


@pytest.mark.django_db
def test_update_ksb_form_loads(authenticated_client, mocker):
    mock_get = mocker.patch('core.views.requests.get')
    fake_ksb = {
        "id": str(uuid4()),
        "name": "Edit Me",
        "description": "Original",
        "ksb_type": 1,
        "completed": True,
        "theme": 2,
    }
    mock_get.return_value.json.return_value = fake_ksb

    url = reverse('update_ksb', args=[fake_ksb['id']])
    response = authenticated_client.get(url)

    assert response.status_code == 200
    assert 'Edit Me' in response.content.decode()
