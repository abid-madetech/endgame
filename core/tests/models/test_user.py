import pytest
from django.urls import reverse
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_user_can_register(client):
    response = client.post(reverse('signup'), {
        'username': 'newuser',
        'password1': 'Testpass123!',
        'password2': 'Testpass123!',
    })
    assert response.status_code == 302  # redirected to login
    assert User.objects.filter(username='newuser').exists()
