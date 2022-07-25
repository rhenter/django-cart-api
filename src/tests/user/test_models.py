import datetime
import pytest
from freezegun import freeze_time


pytestmark = pytest.mark.django_db


def test_user_model_generate_activation_code(admin_user):
    assert admin_user.activation_code == ''
    admin_user.generate_activation_code()
    assert admin_user.activation_code != ''


def test_user_model_generate_activation_code_expiration(admin_user):
    initial_datetime = datetime.datetime(year=2019, month=8, day=12,
                                         hour=15, minute=6, second=3)
    with freeze_time(initial_datetime) as frozen_datetime:
        assert frozen_datetime() == initial_datetime

        activation_code = admin_user.generate_activation_code()
        assert admin_user.activation_code == activation_code

        frozen_datetime.tick(delta=datetime.timedelta(seconds=300))
        assert admin_user.activation_code != admin_user.generate_activation_code()
