import json
import os
import random
import uuid
from datetime import timedelta
from unittest import mock

import pytest
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone
from django.utils.translation import activate
from model_bakery import baker
from oauth2_provider.models import AccessToken, Application
from rest_framework.test import APIClient
import django_models.utils
from .base.conftest import plant_recipe, area_recipe, section_recipe
from .utils import random_json, random_dataframe

activate('en')
content = json.dumps({'asdf': random.random()}, cls=DjangoJSONEncoder).encode('utf-8')

baker.generators.add('django_models.fields.UUIDPrimaryKeyField', uuid.uuid4)
baker.generators.add('apps.core.fields.CompressedJSONField', random_json)
baker.generators.add('picklefield.PickledObjectField', random_dataframe)


def pytest_configure():
    settings.LANGUAGE_CODE = 'en'


@pytest.fixture(scope='module')
def vcr_cassette_dir(request):
    return os.path.join(os.path.dirname(__file__),
                        'fixtures',
                        'cassettes')


@pytest.fixture(scope='session')
def celery_config():
    return {
        'broker_url': 'redis://localhost:6379/0',
        'result_backend': 'redis://localhost:6379/1'
    }


class MockNotification:
    def create(self, *args, **kwargs):
        return True


# @pytest.fixture()
# def mock_redis():
#     server = fakeredis.FakeServer()
#     with mock.patch('redis.Redis', fakeredis.FakeStrictRedis(server=server)) as _fixture:
#         yield _fixture


@pytest.fixture
def admin_client(admin_user):
    application = Application.objects.create(
        name="Test Application",
        redirect_uris="http://localhost https://example.comhttps:///example.org",
        user=admin_user,
        client_type=Application.CLIENT_CONFIDENTIAL,
        authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
    )

    access_token = AccessToken.objects.create(
        user=admin_user,
        scope="read write",
        expires=timezone.now() + timedelta(seconds=300),
        token="secret-access-token-key",
        application=application
    )

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token.token)
    client.force_authenticate(user=admin_user)

    return client


@pytest.fixture(scope='session', autouse=True)
def mock_user_notification():
    with mock.patch('apps.user.models.User.notifications',
                    mock.MagicMock(return_value=MockNotification())) as _fixture:
        yield _fixture


@pytest.fixture
def plant():
    return plant_recipe.make()


@pytest.fixture
def area():
    return area_recipe.make()


@pytest.fixture
def section():
    return section_recipe.make()
