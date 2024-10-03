from django.shortcuts import render
from rest_framework import generics
from movies import models
from .serializers import moviesSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from movies.models import movies as Movie
# Create your views here.

class ListMovie(generics.ListCreateAPIView):
    queryset = models.movies.objects.all()
    serializer_class = moviesSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = self.queryset.all()
        rating_filter = self.request.query_params.get('rating', None)
        if rating_filter is not None:
            queryset = queryset.filter(rating__icontains=rating_filter)
        return queryset

class DetailMovie(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.movies.objects.all()
    serializer_class = moviesSerializer
    permission_classes = [IsAdminUser]

    def post(self, request):
        # Only admin users can create new model instances
        serializer = moviesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MovieViewSet(viewsets.ModelViewSet):
    queryset = models.movies.objects.all()
    serializer_class = moviesSerializer


#API END POINTS BELOW
class MovieListView(APIView):
    def get(self, request):
        movies = Movie.objects.all()
        serializer = moviesSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = moviesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MovieDetailView(APIView):
    def get_object(self, pk):
        try:
            return Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        movie = self.get_object(pk)
        serializer = moviesSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        movie = self.get_object(pk)
        serializer = moviesSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = self.get_object(pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)