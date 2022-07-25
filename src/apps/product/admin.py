from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = [
        'sku',
        'name',
    ]
    search_fields = ('sku', 'name',)
