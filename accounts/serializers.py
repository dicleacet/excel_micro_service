from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from accounts.models import User


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {'no_active_account': _('Bu bilgilere ait üyelik bulunamadı, bilgileri kontrol ediniz.')}

    def create(self, validated_data):
        return UserTokenObtainPairSerializer(**validated_data)

    def update(self, instance, validated_data):
        return UserTokenObtainPairSerializer(**validated_data)


class UserTokenRefreshSerializer(TokenRefreshSerializer):

    def create(self, validated_data):
        return UserTokenRefreshSerializer(**validated_data)

    def update(self, instance, validated_data):
        return UserTokenRefreshSerializer(**validated_data)


class UserTokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.ReadOnlyField()

    def create(self, validated_data):
        return UserTokenRefreshResponseSerializer(**validated_data)

    def update(self, instance, validated_data):
        return UserTokenRefreshResponseSerializer(**validated_data)

