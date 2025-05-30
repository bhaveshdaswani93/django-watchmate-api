from django.shortcuts import render
from django.http import JsonResponse
from watchlist_app.models import Movie

# Create your views here.

def movie_list(request):
    movies = Movie.objects.all()
    data = {'data': list(movies.values())}
    
    
    return JsonResponse(data)

def movie_detail(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)
        data = {
            'id': movie.id,
            'name': movie.name,
            'description': movie.description,
            'active': movie.active
        }
        return JsonResponse(data)
    except Movie.DoesNotExist:
        return JsonResponse({'error': 'Movie not found'}, status=404)
    
