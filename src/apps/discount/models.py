from functools import partial

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_models.utils.generators import generate_random_code

from apps.core.models import BaseModel

generate_code = partial(generate_random_code, length=6)


class DiscountCoupon(BaseModel):
    code = models.CharField(
        max_length=16, default=generate_code, verbose_name=_('Code'), unique=True,
        help_text=_('Discount Coupon Identifier')
    )
    value = models.DecimalField(
        decimal_places=2, max_digits=9, help_text=_('Value')
    )
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.code} - {self.value}'
