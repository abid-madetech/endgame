from uuid import uuid4

import pytest
from django.urls import reverse
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_any_user_can_access_view_ksb_page(client):
    fake_id = str(uuid4())
    response = client.get(reverse('view_ksb', args=[fake_id]))
    assert response.status_code == 200
    assert 'View KSB' in response.content.decode()