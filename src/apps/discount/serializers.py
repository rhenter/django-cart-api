from rest_framework import serializers

from .models import DiscountCoupon


class DiscountCouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCoupon
        fields = (
            'id',
            'code',
            'value',
            'is_active',
            'created_at',
        )
        read_only_fields = (
            'id',
        )
