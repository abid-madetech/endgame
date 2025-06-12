from uuid import uuid4

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_any_user_can_access_view_ksb_page(client):
    fake_id = str(uuid4())
    response = client.get(reverse('view_ksb', args=[fake_id]))
    assert response.status_code == 200
    assert 'View KSB' in response.content.decode()

@pytest.mark.django_db
def test_view_ksb_page_loads(client, mocker):
    fake_id = str(uuid4())
    mock_data = {
        "id": fake_id,
        "name": "Test KSB",
        "description": "Test description",
        "ksb_type": 1,
        "theme": None,
        "completed": False,
        "last_updated": "2025-06-01T10:00:00Z"
    }

    mock_get = mocker.patch('core.views.requests.get')
    mock_get.return_value.json.return_value = mock_data
    mock_get.return_value.status_clode = 200

    response = client.get(reverse('view_ksb', args=[fake_id]))
    assert response.status_code == 200
    assert "Test KSB" in response.content.decode()

@pytest.mark.django_db
def test_view_actions_are_available(client, mocker):
    fake_id = str(uuid4())
    mock_data = {
        "id": fake_id,
        "name": "Test KSB",
        "description": "Test description",
        "ksb_type": 1,
        "theme": None,
        "completed": False,
        "last_updated": "2025-06-01T10:00:00Z"
    }

    mock_get = mocker.patch('core.views.requests.get')
    mock_get.return_value.json.return_value = mock_data
    mock_get.return_value.status_clode = 200

    response = client.get(reverse('view_ksb', args=[fake_id]))
    assert response.status_code == 200
    assert "Back to all KSBs" in response.content.decode()


@pytest.mark.django_db
def test_ksb_view_doesnt_render_edit_delete_actions(client, mocker):
    mocker.patch('core.views.requests.get')
    fake_id = str(uuid4())
    response = client.get(reverse('view_ksb', args=[fake_id]))

    assert response.status_code == 200
    assert 'Edit' not in response.content.decode()
    assert 'Delete' not in response.content.decode()
