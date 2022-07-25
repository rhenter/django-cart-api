from django.contrib import admin

from apps.cart.models import Cart, CartProduct


class CartProductInline(admin.TabularInline):
    model = CartProduct
    classes = ['collapse']
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    model = Cart
    list_display = [
        'id',
        'user',
        'created_at',
        'is_active',
    ]
    inlines = [CartProductInline]
