from functools import partial

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_models.utils.generators import generate_random_code

from apps.core.models import BaseModel

generate_code = partial(generate_random_code, length=16)


class Cart(BaseModel):
    user = models.ForeignKey(
        'user.User',
        related_name='carts',
        on_delete=models.CASCADE,
        verbose_name=_('Cart'),
    )
    is_active = models.BooleanField(default=True, verbose_name=_('Is Active'))

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.id} - {self.created_at}'


class CartProduct(BaseModel):
    cart = models.ForeignKey(
        Cart,
        related_name='products',
        on_delete=models.CASCADE,
        verbose_name=_('Cart'),
    )
    product = models.ForeignKey(
        'product.Product',
        related_name='carts',
        on_delete=models.CASCADE,
        verbose_name=_('Product'),
    )
    quantity = models.PositiveIntegerField()

    class Meta:
        ordering = ['product__name']

    def __str__(self):
        return f'{self.cart}-{self.product} qt:{self.quantity}'
