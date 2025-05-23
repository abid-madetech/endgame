import pytest
from rest_framework.test import APIClient
from core.models import KSB, KSBType

@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
def test_get_all_ksbs(client):
    response = client.get("/api/ksbs/")
    assert response.status_code == 200
    assert any(ksb["name"] == "K1" for ksb in response.data)


@pytest.mark.django_db
def test_get_single_ksb(client):
    ksb = KSB.objects.get(name="K1")
    response = client.get(f"/api/ksbs/{ksb.id}/")
    assert response.status_code == 200
    assert response.data["name"] == "K1"


@pytest.mark.django_db
def test_filter_by_ksb_type_id(client):
    knowledge_type = KSBType.objects.get(name__iexact="knowledge")
    response = client.get(f"/api/ksbs/?ksb_type={knowledge_type.id}")
    assert response.status_code == 200
    assert all(KSB.objects.get(id=item["id"]).ksb_type_id == knowledge_type.id for item in response.data)


@pytest.mark.django_db
def test_filter_by_completed(client):
    response = client.get("/api/ksbs/?completed=false")
    assert response.status_code == 200
    assert all(item["completed"] is False for item in response.data)


@pytest.mark.django_db
def test_order_by_name(client):
    response = client.get("/api/ksbs/?ordering=name")
    assert response.status_code == 200
    names = [item["name"] for item in response.data]
    assert names == sorted(names)


@pytest.mark.django_db
def test_order_by_last_updated_desc(client):
    response = client.get("/api/ksbs/?ordering=-last_updated")
    assert response.status_code == 200
    timestamps = [item["last_updated"] for item in response.data]
    assert timestamps == sorted(timestamps, reverse=True)
