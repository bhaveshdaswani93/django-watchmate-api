from rest_framework.authtoken import views
from django.urls import path

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token, name='api_token_auth'),
]