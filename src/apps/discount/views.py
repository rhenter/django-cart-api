import logging

from apps.core.viewsets import BaseViewSet
from .models import DiscountCoupon
from .serializers import DiscountCouponSerializer

logger = logging.getLogger(__name__)


class DiscountCouponViewSet(BaseViewSet):
    serializer_class = DiscountCouponSerializer
    queryset = DiscountCoupon.objects.all()
    lookup_field = 'code'
    search_fields = (
        'code',
    )
    ordering_fields = (
        '-created_at',
        'created_at',
    )
    ordering = ('-created_at',)
