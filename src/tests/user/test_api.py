import json

import pytest
from django.urls import reverse
from rest_framework import status

from apps.user.models import User
from .factories import UserFactory

pytestmark = pytest.mark.django_db


def test_user_api_validate_activation_code_valid(admin_client, admin_user):
    url = reverse('api-user:validate-activation-code')

    data = {
        'user_id': admin_user.id,
        'activation_code': admin_user.generate_activation_code()
    }
    response = admin_client.post(
        url,
        data=json.dumps(data),
        content_type="application/json")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['user_id'] == admin_user.id
    assert response.json()['activation_code'] == admin_user.activation_code


@pytest.mark.parametrize('value,error_expected', [
    ('invalid', 'Ensure this field has no more than 6 characters.'),
    ('invali', 'Activation Code Invalid.'),
    ('123123', 'Activation Code Invalid.'),
    ('123', 'Ensure this field has at least 6 characters.'),
    ('123123123123123', 'Ensure this field has no more than 6 characters.'),
])
def test_user_api_validate_activation_code_invalid(
        value, error_expected, admin_client, admin_user):
    url = reverse('api-user:validate-activation-code')

    data = {
        'user_id': admin_user.id,
        'activation_code': value
    }
    response = admin_client.post(
        url,
        data=json.dumps(data),
        content_type="application/json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['activation_code'] == [error_expected]


def test_user_api_list(admin_client):
    users_count = 5
    users_plus_admin_count = users_count + 1
    UserFactory.create_batch(users_count)

    url = reverse('api-user:users-list')
    response = admin_client.get(url, content_type="application/json")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['count'] == users_plus_admin_count
    assert User.objects.count() == users_plus_admin_count


def test_user_api_detail(admin_client, admin_user):
    url = reverse('api-user:users-detail', args=[admin_user.id])
    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == admin_user.id
    assert response.json()['name'] == admin_user.get_full_name()


def test_user_api_post(admin_client, user_data):
    url = reverse('api-user:users-list')
    response = admin_client.post(url, data=user_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['email'] == user_data['email']
    assert User.objects.filter(email=user_data['email']).exists()


def test_user_api_patch(admin_client, admin_user):
    data = {'first_name': 'User'}
    url = reverse('api-user:users-detail', args=[admin_user.id])
    response = admin_client.patch(
        url,
        data=json.dumps(data),
        content_type='application/json')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['first_name'] == data['first_name']
    assert User.objects.filter(first_name=data['first_name']).exists()


def test_user_api_put(admin_client, admin_user):
    data = admin_user.serialize()
    data['first_name'] = 'User'
    data['email'] = 'test@test.com'
    url = reverse('api-user:users-detail', args=[admin_user.id])
    response = admin_client.put(
        url,
        data=json.dumps(data),
        content_type='application/json')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['first_name'] == data['first_name']
    assert User.objects.filter(first_name=data['first_name']).exists()
