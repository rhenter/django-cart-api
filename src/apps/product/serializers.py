from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'sku',
            'name',
            'is_active',
        )
        read_only_fields = (
            'id',
            'sku',
        )
