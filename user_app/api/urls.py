from rest_framework.authtoken import views
from django.urls import path

from user_app.api.views import register_user, logout_user

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token, name='api_token_auth'),
    path('register/', register_user, name='register_user'),
    path('logout/', logout_user, name='logout_user'),
]