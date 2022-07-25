from rest_framework import serializers

from .models import User


class UserDetailSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='get_full_name', required=False)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'name',
            'cellphone',
            'email',
            'is_superuser',
            'is_active',
            'last_login',
        ]


class UserCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'cellphone',
            'email',
            'is_superuser',
            'is_active',
        ]
        read_only_fields = (
            'id',
            'is_superuser',
            'is_active',
        )
