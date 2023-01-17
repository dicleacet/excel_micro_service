from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.UserObtainTokenPairView.as_view(), name='login'),
    path('login/refresh/', views.UserTokenRefreshView.as_view(), name='login_refresh'),
]

