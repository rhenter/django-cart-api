import logging

from rest_framework import status
from rest_framework.response import Response

from apps.core.viewsets import BaseViewSet
from .models import Cart, CartProduct
from .serializers import CartCreateProductSerializer, CartCreateSerializer, CartProductSerializer, CartSerializer

logger = logging.getLogger(__name__)


class CartViewSet(BaseViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    ordering_fields = (
        '-created_at',
        'created_at',
    )
    ordering = ('-created_at',)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CartCreateSerializer
        return self.serializer_class

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data
        data['user'] = request.user.id

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CartProductViewSet(BaseViewSet):
    serializer_class = CartProductSerializer
    queryset = CartProduct.objects.all()
    search_fields = (
        'product__name',
    )

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CartCreateProductSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        data = request.data
        if 'cart' not in data:
            cart = Cart.objects.create(user=request.user)
            data['cart'] = cart.id

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
