import pytest
from rest_framework.test import APIClient
from core.models import KSBType

@pytest.fixture
def client():
    return APIClient()

@pytest.mark.django_db
def test_get_all_ksb_types(client):
    response = client.get("/api/ksb-types/")
    assert response.status_code == 200
    assert {t["name"].lower() for t in response.data} == {"knowledge", "skill", "behaviour"}

@pytest.mark.django_db
def test_get_single_ksb_type(client):
    ksb_type = KSBType.objects.get(name__iexact="knowledge")
    response = client.get(f"/api/ksb-types/{ksb_type.id}/")
    assert response.status_code == 200
    assert response.data["name"].lower() == "knowledge"
