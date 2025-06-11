from django.urls import path
from watchlist_app.api import views

urlpatterns = [
    path('lists', views.WatchListAV.as_view(), name='watch-list'),
    path('lists/<int:pk>', views.WatchListDetailAV.as_view(), name='watch-list-detail'),
    path('platforms', views.StreamPlatformListAV.as_view(), name='stream-platform-list'),
    path('platforms/<int:pk>', views.StreamPlatformDetailAV.as_view(), name='streamplatform-detail'),
    path('stream/<int:pk>/reviews', views.ReviewList.as_view(), name='review-list'),
    path('stream/reviews/<int:pk>', views.ReviewDetail.as_view(), name='review-detail'),

]