from rest_condition import Or
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

SYSADMIN_GROUP = 'admin'


class AuthViewSet:
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [Or(IsAuthenticated, )]


class BaseViewSet(AuthViewSet, ModelViewSet):
    pass
