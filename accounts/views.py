from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import AllowAny, IsAuthenticated, SAFE_METHODS
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from accounts import serializers


class UserObtainTokenPairView(TokenObtainPairView):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = serializers.UserTokenObtainPairSerializer

    @extend_schema(tags=['Users - Public'], responses=serializers.UserTokenRefreshSerializer)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserTokenRefreshView(TokenRefreshView):
    authentication_classes = []
    permission_classes = [AllowAny]
    serializer_class = serializers.UserTokenRefreshSerializer

    @extend_schema(tags=['Users - Public'], responses=serializers.UserTokenRefreshResponseSerializer)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

