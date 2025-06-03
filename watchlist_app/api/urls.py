from django.urls import path
from watchlist_app.api import views

urlpatterns = [
    path('lists', views.movie_list, name='movie-list'),
    path('lists/<int:pk>', views.movie_detail, name='movie-detail'),
]