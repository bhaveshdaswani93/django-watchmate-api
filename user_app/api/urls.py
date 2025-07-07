from rest_framework.authtoken import views
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from user_app.api.views import register_user, logout_user

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('api-token-auth/', views.obtain_auth_token, name='api_token_auth'),
    path('logout/', logout_user, name='logout_user'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]