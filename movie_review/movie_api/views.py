from django.shortcuts import render
from rest_framework import generics
from movies import models
from .serializers import moviesSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework.response import Response
from movies.models import Movie
from rest_framework.decorators import api_view
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination #this makes me import to allow pagination
# Create your views here.

# the below code is what helps to handle pagination. This class defines the pagination settings, such as the page size, page size query parameter, and maximum page size.
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class moviesListCreateAPIview(generics.ListCreateAPIView):
    queryset = models.Movie.objects.all()
    serializer_class = moviesSerializer
    permission_classes = [IsAuthenticated]
     #below is the ordering and filter i added
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['rating', 'created_at']
    search_fields = ['title']
    pagination_class = StandardResultsSetPagination #the pagination class i used

    def get_queryset(self):
        queryset = self.queryset
        rating_filter = self.request.query_params.get('rating')
        if rating_filter is not None:
            queryset = queryset.filter(rating__icontains=rating_filter)
        return queryset

    def post(self, request):
        serializer = moviesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class moviesRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Movie.objects.all()
    serializer_class = moviesSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def get_object(self, pk):
        try:
            return Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        movie = self.get_object(pk)
        if movie is None:
            return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = moviesSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        movie = self.get_object(pk)
        if movie is None:
            return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = moviesSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = self.get_object(pk)
        if movie is None:
            return Response({"error": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    