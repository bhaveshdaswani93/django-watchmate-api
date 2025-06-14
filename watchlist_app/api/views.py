# Create your views here.
from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView 
from rest_framework import generics 
from rest_framework import mixins 
from rest_framework import viewsets 
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from watchlist_app.api.permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly

class ReviewList(generics.ListCreateAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Allow unauthenticated users to read, but authenticated users to create

    def get_queryset(self):
        """
        Optionally filter reviews by the watchlist item they belong to.
        """
        watchlist_id = self.kwargs.get('pk')
        if watchlist_id:
            return Review.objects.filter(watchlist=watchlist_id)
        return Review.objects.all()
        # if watchlist_id:
            # return self.queryset.filter(watchlist__id=watchlist_id)
        # return self.queryset
    
    def perform_create(self, serializer):
        """
        Override the perform_create method to set the watchlist
        item for the review.
        """
        watchlist_id = self.kwargs.get('pk')
        watchlist_item = WatchList.objects.get(id=watchlist_id)
        user = self.request.user  # Get the user from the request
        # Check if the user has already reviewed this watchlist item
        if Review.objects.filter(watchlist=watchlist_item, review_user=user).exists():
            raise ValidationError("You have already reviewed this watchlist item.")

        serializer.save(watchlist=watchlist_item, review_user=user)



class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]  # Custom permission to allow only the owner to update or delete

# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# class ReviewDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]  # Allow unauthenticated users to read, but authenticated users to create
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
    
class StreamPlatformModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]  # Add your permission classes here if needed
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    lookup_field = 'pk'  # Default is 'pk', but can be changed to 'slug' or any other field if needed

    # def get_serializer_context(self):
    #     return {'request': self.request}
    
    # def perform_create(self, serializer):
    #     serializer.save()

class StreamPlatformViewSet(viewsets.ViewSet):
    def list (self, request):
        platforms = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platforms, many=True, context={'request': request})
        data = {'data': serializer.data}
        return Response(data)

    def create(self, request):
        serializer = StreamPlatformSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Stream Platform not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StreamPlatformSerializer(platform, context={'request': request})
        data = {'data': serializer.data}
        return Response(data)

    

class StreamPlatformListAV(APIView):
    def get(self, request):
        platforms = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platforms, many=True, context={'request': request})
        data = {'data': serializer.data}
        return Response(data)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data, context={'request': request})
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
        
        serializer = StreamPlatformSerializer(platform, context={'request': request})
        data = {'data': serializer.data}
        return Response(data)

    def put(self, request, pk):
        platform = self.get_object(pk)
        if platform is None:
            return Response({'error': 'Stream Platform not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StreamPlatformSerializer(platform, data=request.data, context={'request': request})
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