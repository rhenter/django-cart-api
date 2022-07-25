import logging

from apps.core.viewsets import BaseViewSet
from .models import Product
from .serializers import ProductSerializer

logger = logging.getLogger(__name__)


class ProductViewSet(BaseViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'sku'
    search_fields = (
        'name',
    )
    ordering_fields = (
        '-created_at',
        '-name',
        'created_at',
        'name',
    )
    ordering = ('-created_at',)
