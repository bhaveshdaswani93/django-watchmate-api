# Create your views here.
from django_filters import rest_framework as filters
from rest_framework import filters as drf_filters
from rest_framework import generics 
from rest_framework import mixins 
from rest_framework import status
from rest_framework import viewsets 
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from rest_framework.views import APIView 

from watchlist_app.api import (pagination, 
                               permissions, 
                               serializers, 
                               throttles)

from watchlist_app import models

class ReviewList(generics.ListCreateAPIView):
    serializer_class = serializers.ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Allow unauthenticated users to read, but authenticated users to create
    # throttle_classes = [ScopedRateThrottle]
    # throttle_scope = 'reviewlist'   # Custom throttle scope for this view

    def get_queryset(self):
        """
        Optionally filter reviews by the watchlist item they belong to.
        """
        watchlist_id = self.kwargs.get('pk')
        if watchlist_id:
            return models.Review.objects.filter(watchlist=watchlist_id)
        return models.Review.objects.all()
    
    def perform_create(self, serializer):
        """
        Override the perform_create method to set the watchlist
        item for the review.
        """
        watchlist_id = self.kwargs.get('pk')
        watchlist_item = models.WatchList.objects.get(id=watchlist_id)
        user = self.request.user  # Get the user from the request
        # Check if the user has already reviewed this watchlist item
        if models.Review.objects.filter(watchlist=watchlist_item, review_user=user).exists():
            raise ValidationError("You have already reviewed this watchlist item.")
        
        watchlist_item.num_of_ratings += 1
        watchlist_item.avg_rating = (watchlist_item.avg_rating * (watchlist_item.num_of_ratings - 1) + serializer.validated_data['rating']) / watchlist_item.num_of_ratings
        watchlist_item.save()

        serializer.save(watchlist=watchlist_item, review_user=user)



class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = [permissions.IsOwnerOrReadOnly]  # Custom permission to allow only the owner to update or delete

class WatchListGenericsListAV(generics.ListAPIView):
    # permission_classes = [permissions.IsAdminOrReadOnly]  # Allow unauthenticated users to read, but authenticated users to create
    # throttle_classes = [throttles.WatchListThrottle]  # Apply throttling to the view
    queryset = models.WatchList.objects.all()
    serializer_class = serializers.StreamPlatformSerializer
    # filter_backends = [filters.DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]  # Enable filtering, searching, and ordering
    # ordering_fields = ['title', 'platform__name']  # Allow ordering by title and platform name
    # filterset_fields = ['title', 'platform__name']  # Allow filtering by name and platform name
    # search_fields = ['title', 'platform__name']  # Allow searching by title and platform name
    pagination_class = pagination.WatchListPagination

class WatchListAV(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]  # Allow unauthenticated users to read, but authenticated users to create
    throttle_classes = [throttles.WatchListThrottle]  # Apply throttling to the view
    def get(self, request):
        watch_list = models.WatchList.objects.all()
        serializer = serializers.WatchListSerializer(watch_list, many=True)
        data = {'data': serializer.data}
        return Response(data)

    def post(self, request):
        print("Data received:", request.data)  # Debugging line to check incoming data
        serializer = serializers.WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class WatchListDetailAV(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]  # Allow unauthenticated users to read, but authenticated users to create
    throttle_classes = [throttles.WatchListDetailThrottle]  # Apply throttling to the view
    def get_object(self, pk):
        try:
            return models.WatchList.objects.get(pk=pk)
        except models.WatchList.DoesNotExist:
            return None

    def get(self, request, pk):
        watch_list = self.get_object(pk)
        if watch_list is None:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = serializers.WatchListSerializer(watch_list)
        data = {'data': serializer.data}
        return Response(data)

    def put(self, request, pk):
        watch_list = self.get_object(pk)
        if watch_list is None:
            return Response({'error': 'Watch List not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = serializers.WatchListSerializer(watch_list, data=request.data)
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
    permission_classes = [permissions.IsAdminOrReadOnly]  # Add your permission classes here if needed
    queryset = models.StreamPlatform.objects.all()
    serializer_class = serializers.StreamPlatformSerializer
    lookup_field = 'pk'  # Default is 'pk', but can be changed to 'slug' or any other field if needed

class StreamPlatformViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAdminOrReadOnly]  # Add your permission classes here if needed
    def list (self, request):
        platforms = models.StreamPlatform.objects.all()
        serializer = serializers.StreamPlatformSerializer(platforms, many=True, context={'request': request})
        data = {'data': serializer.data}
        return Response(data)

    def create(self, request):
        serializer = serializers.StreamPlatformSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            platform = models.StreamPlatform.objects.get(pk=pk)
        except models.StreamPlatform.DoesNotExist:
            return Response({'error': 'Stream Platform not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = serializers.StreamPlatformSerializer(platform, context={'request': request})
        data = {'data': serializer.data}
        return Response(data)

    

class StreamPlatformListAV(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]  # Allow unauthenticated users to read, but authenticated users to create
    def get(self, request):
        platforms = models.StreamPlatform.objects.all()
        serializer = serializers.StreamPlatformSerializer(platforms, many=True, context={'request': request})
        data = {'data': serializer.data}
        return Response(data)

    def post(self, request):
        serializer = serializers.StreamPlatformSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class StreamPlatformDetailAV(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]  # Allow unauthenticated users to read, but authenticated users to create
    def get_object(self, pk):
        try:
            return models.StreamPlatform.objects.get(pk=pk)
        except models.StreamPlatform.DoesNotExist:
            return None

    def get(self, request, pk):
        platform = self.get_object(pk)
        if platform is None:
            return Response({'error': 'Stream Platform not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = serializers.StreamPlatformSerializer(platform, context={'request': request})
        data = {'data': serializer.data}
        return Response(data)

    def put(self, request, pk):
        platform = self.get_object(pk)
        if platform is None:
            return Response({'error': 'Stream Platform not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = serializers.StreamPlatformSerializer(platform, data=request.data, context={'request': request})
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

class UserReviewList(generics.ListAPIView):
    serializer_class = serializers.ReviewSerializer
    # permission_classes = [IsAuthenticated]  # Ensure the user is authenticated to view their reviews

    def get_queryset(self):
        """
        We need to get username from the url parameter and then filter by id.
        """
        username = self.kwargs.get('username')
        return models.Review.objects.filter(review_user__username=username)

class UserReviewListQueryParam(generics.ListAPIView):
    serializer_class = serializers.ReviewSerializer
    # permission_classes = [IsAuthenticated]  # Ensure the user is authenticated to view their reviews

    def get_queryset(self):
        """
        We need to get the username from the query parameters and then filter by it.
        """
        username = self.request.query_params.get('username')
        return models.Review.objects.filter(review_user__username=username)