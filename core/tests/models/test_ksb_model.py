import pytest
from core.models import KSB, KSBType
from django.db import IntegrityError, transaction

@pytest.mark.django_db
def test_create_ksb():
    knowledge = KSBType.objects.get(id=1)
    ksb = KSB.objects.create(name="K111", description="test", ksb_type=knowledge)
    assert ksb.description == "test"
    assert ksb.name == "K111"
    assert ksb.completed == False
    assert ksb.ksb_type.name == "Knowledge"

@pytest.mark.django_db
def test_ensure_name_and_desc_are_unique():
    knowledge = KSBType.objects.get(id=1)
    KSB.objects.create(name="K111", description="test", ksb_type=knowledge)
    # Check duplicate name
    with pytest.raises(IntegrityError):
        with transaction.atomic():
            KSB.objects.create(name="K111", description="desc", ksb_type=knowledge)

    # Check duplicate description
    with pytest.raises(IntegrityError):
        with transaction.atomic():
            KSB.objects.create(name="K2", description="test", ksb_type=knowledge)