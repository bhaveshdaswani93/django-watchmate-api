# Create your views here.
from watchlist_app.models import WatchList, StreamPlatform
from watchlist_app.api.serializers import WatchListSerializer, StreamPlatformSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView 

class WatchListAV(APIView):
    def get(self, request):
        watch_list = WatchList.objects.all()
        serializer = WatchListSerializer(watch_list, many=True)
        data = {'data': serializer.data}
        return Response(data)

    def post(self, request):
        print("Data received:", request.data)  # Debugging line to check incoming data
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class WatchListDetailAV(APIView):
    def get_object(self, pk):
        try:
            return WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return None

    def get(self, request, pk):
        watch_list = self.get_object(pk)
        if watch_list is None:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = WatchListSerializer(watch_list)
        data = {'data': serializer.data}
        return Response(data)

    def put(self, request, pk):
        watch_list = self.get_object(pk)
        if watch_list is None:
            return Response({'error': 'Watch List not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = WatchListSerializer(watch_list, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        watch_list = self.get_object(pk)
        if watch_list is None:
            return Response({'error': 'Watch List not found'}, status=status.HTTP_404_NOT_FOUND)
        
        watch_list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class StreamPlatformListAV(APIView):
    def get(self, request):
        platforms = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platforms, many=True)
        data = {'data': serializer.data}
        return Response(data)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class StreamPlatformDetailAV(APIView):
    def get_object(self, pk):
        try:
            return StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return None

    def get(self, request, pk):
        platform = self.get_object(pk)
        if platform is None:
            return Response({'error': 'Stream Platform not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StreamPlatformSerializer(platform)
        data = {'data': serializer.data}
        return Response(data)

    def put(self, request, pk):
        platform = self.get_object(pk)
        if platform is None:
            return Response({'error': 'Stream Platform not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StreamPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        platform = self.get_object(pk)
        if platform is None:
            return Response({'error': 'Stream Platform not found'}, status=status.HTTP_404_NOT_FOUND)
        
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method == 'POST':
#         print("Data received:", request.data)  # Debugging line to check incoming data
#         serializer = WatchListSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     # If the request method is GET, return the list of movies
#     movies = Movie.objects.all()
#     serializer = WatchListSerializer(movies, many=True)
#     data = {'data': serializer.data}
#     return Response(data)

# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_detail(request, pk):
#     try:
#         movie = Movie.objects.get(pk=pk)
#     except Movie.DoesNotExist:
#         return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == 'PUT':
#         serializer = WatchListSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#     serializer = WatchListSerializer(movie)
#     data = {'data': serializer.data}
#     return Response(data)