from django.urls import path
from watchlist_app.api import views

urlpatterns = [
    path('lists', views.MovieListAV.as_view(), name='movie-list'),
    path('lists/<int:pk>', views.MovieDetailAV.as_view(), name='movie-detail'),
]