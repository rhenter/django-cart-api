import logging

from rest_framework.permissions import AllowAny

from apps.core.viewsets import BaseViewSet
from .models import User
from .serializers import (
    UserCreateUpdateSerializer,
    UserDetailSerializer
)

logger = logging.getLogger(__name__)


class UserViewSet(BaseViewSet):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = 'id'
    filterset_fields = ('first_name',)
    search_fields = (
        'first_name',
        'last_name',
        'email',
    )
    ordering_fields = (
        '-date_joined',
        '-name',
        'date_joined',
        'first_name',
    )
    ordering = ('-date_joined',)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return UserCreateUpdateSerializer
        return self.serializer_class
