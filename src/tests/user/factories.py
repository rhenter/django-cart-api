import factory
import pytest
from factory.django import DjangoModelFactory

from apps.user.models import User
from ..utils import fake

pytestmark = pytest.mark.django_db


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    is_superuser = True
    username = factory.Sequence(
        lambda n: "{}%03d".format(
            fake.user_name()) %
        n)
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    is_staff = True
    is_active = True
    cellphone = fake.cellphone_number()

