from functools import partial

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_models.utils.generators import generate_random_code

from apps.core.models import BaseModel

generate_code = partial(generate_random_code, length=6)


class Product(BaseModel):
    sku = models.CharField(
        max_length=16, default=generate_code, verbose_name='SKU', unique=True,
        help_text=_('Product identifier')
    )
    name = models.CharField(
        max_length=128, unique=True, help_text=_('Product name'), verbose_name=_('Name')
    )
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.sku} - {self.name}'
