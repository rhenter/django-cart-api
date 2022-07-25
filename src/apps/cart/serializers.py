from rest_framework import serializers

from .models import Cart, CartProduct


class CartCreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = (
            'id',
            'cart',
            'product',
            'quantity'
        )
        read_only_fields = (
            'id',
        )


class CartProductSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.name')

    class Meta:
        model = CartProduct
        fields = (
            'id',
            'cart',
            'product',
            'quantity'
        )
        read_only_fields = (
            'id',
        )


class CartCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = (
            'id',
            'user',
        )
        read_only_fields = (
            'id',
        )


class CartSerializer(serializers.ModelSerializer):
    products = CartProductSerializer(many=True, required=False)
    user = serializers.CharField(source='user.get_full_name')

    class Meta:
        model = Cart
        fields = (
            'id',
            'user',
            'is_active',
            'created_at',
            'products',
        )
        read_only_fields = (
            'id',
        )
