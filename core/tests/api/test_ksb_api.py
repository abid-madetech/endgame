import pytest
from rest_framework.test import APIClient
from core.models import KSB

@pytest.mark.django_db
def test_get_all_ksbs():
    client  = APIClient()
    response = client.get("/api/ksbs/")
    assert response.status_code == 200
    assert response.data[0]['name'] == "K1"