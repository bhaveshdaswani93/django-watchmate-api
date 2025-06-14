from django.urls import path, include
from rest_framework.routers import DefaultRouter
from watchlist_app.api import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register('platforms', views.StreamPlatformModelViewSet, basename='platforms')


urlpatterns = [
    path('lists', views.WatchListAV.as_view(), name='watch-list'),
    path('lists/<int:pk>', views.WatchListDetailAV.as_view(), name='watch-list-detail'),
    path('', include(router.urls)),  # Include the router's URLs
    # path('platforms', views.StreamPlatformListAV.as_view(), name='stream-platform-list'),
    # path('platforms/<int:pk>', views.StreamPlatformDetailAV.as_view(), name='streamplatform-detail'),
    path('<int:pk>/reviews', views.ReviewList.as_view(), name='review-list'),
    path('reviews/<int:pk>', views.ReviewDetail.as_view(), name='review-detail'),

]