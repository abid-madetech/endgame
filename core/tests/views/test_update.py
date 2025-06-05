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
    response = authenticated_client.get(reverse('create_ksb'))
    assert response.status_code == 200
    assert 'Create KSB' in response.content.decode()


# @pytest.mark.django_db
# def test_create_ksb_submits_to_api(authenticated_client, mocker):
#     mock_post = mocker.patch('core.views.requests.post')
#     mock_post.return_value.status_code = 201
#
#     response = authenticated_client.post(reverse('create_ksb'), {
#         'name': 'Test KSB',
#         'description': 'testing',
#         'ksb_type': 1,
#         'theme_id': 1,
#         'completed': '1'
#     })
#
#     assert response.status_code == 302  # Redirect after success
#     mock_post.assert_called_once()
#     payload = mock_post.call_args[1]['json']
#     assert payload['name'] == 'Test KSB'
#     assert payload['ksb_type'] == 1
