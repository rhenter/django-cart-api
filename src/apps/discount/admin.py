from django.contrib import admin

from apps.discount.models import DiscountCoupon


@admin.register(DiscountCoupon)
class DiscountCouponAdmin(admin.ModelAdmin):
    model = DiscountCoupon
    list_display = [
        'id',
        'code',
        'value',
        'created_at',
        'is_active',
    ]
    search_fields = ('code', 'value',)
