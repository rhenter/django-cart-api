from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_models.models import SignalsModel
from django_models.utils import remove_special_characters

from apps.core.models import BaseModel
from .managers import UserSignalsManager


class User(SignalsModel, AbstractUser):
    cellphone = models.CharField(max_length=20, blank=True)

    objects = UserSignalsManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return f'{self.get_full_name()}'

    def _clean_phone(self, value):
        number = remove_special_characters(value.replace(' ', ''))

        if number.startswith('0'):
            number = number[1:]
        return number

    def pre_save(self, save_kwargs):
        self.cellphone = self._clean_phone(self.cellphone)
