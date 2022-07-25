from model_bakery.recipe import Recipe, foreign_key
from model_bakery import seq
import pytest
from apps.user.models import User

user_recipe = Recipe(
    User,
    cellphone=seq('21921212121 '),
    email=seq('user@test.com'),
    first_name=seq('Test'),
    last_name=seq('System User'),
    username=seq('usertest'),
)


@pytest.fixture
def user_data():
    return {
        'cellphone': '21921212121',
        'email': 'user@test.com',
        'first_name': 'Test',
        'last_name': 'System User',
        'phone': '21 1212121212',
        'sex': 'm',
        'username': 'usertest',
    }
