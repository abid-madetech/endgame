import pytest
from core.models import KSBType

@pytest.mark.django_db
def test_create_ksb_type():
    ksb_type = KSBType.objects.create(id=10, name="testType")
    assert ksb_type.id == 10
    assert ksb_type.name == "testType"

@pytest.mark.django_db
def test_ksb_type_name():
    ksb_type = KSBType.objects.get(id=2)
    assert str(ksb_type) == "Skill"

@pytest.mark.django_db
def test_ksb_types_are_seeded():
    assert KSBType.objects.filter(name="Skill").exists()
    assert KSBType.objects.filter(name="Knowledge").exists()
    assert KSBType.objects.filter(name="Behaviour").exists()
