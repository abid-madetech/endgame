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
def test_ksbs_list_renders_correctly(authenticated_client, mocker):
    mock_get = mocker.patch('core.views.requests.get')
    mock_get.return_value.json.return_value = [
        {
            "id": "123",
            "name": "KSB 1",
            "description": "A skill",
            "completed": False,
            "ksb_type": 1,
            "theme": {
                "id": 1,
                "name": "Code Quality"
            },
            "last_updated": "2025-05-01T10:00:00Z"
        }
    ]

    response = authenticated_client.get(reverse('home'))

    assert response.status_code == 200
    assert 'KSB 1' in response.content.decode()
    assert 'A skill' in response.content.decode()
    assert 'Theme' in response.content.decode() #has theme column
    assert 'Code Quality' in response.content.decode() #has theme name

@pytest.mark.django_db
def test_create_ksb_requires_auth(client):
    response = client.get(reverse('create_ksb'))
    assert response.status_code == 302

@pytest.mark.django_db
def test_authenticated_user_can_access_create_page(authenticated_client):
    response = authenticated_client.get(reverse('create_ksb'))
    assert response.status_code == 200
    assert 'Create KSB' in response.content.decode()

@pytest.mark.django_db
def test_create_ksb_submits_to_api(authenticated_client, mocker):
    mock_post = mocker.patch('core.views.requests.post')
    mock_post.return_value.status_code = 201

    response = authenticated_client.post(reverse('create_ksb'), {
        'name': 'Test KSB',
        'description': 'testing',
        'ksb_type': 1,
        'theme_id': 1,
        'completed': '1'
    })

    assert response.status_code == 302  # Redirect after success
    mock_post.assert_called_once()
    payload = mock_post.call_args[1]['json']
    assert payload['name'] == 'Test KSB'
    assert payload['ksb_type'] == 1


