from django.shortcuts import render
from rest_framework import generics
from movies import models
from .serializers import moviesSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
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

class MovieViewSet(viewsets.ModelViewSet):
    queryset = models.movies.objects.all()
    serializer_class = moviesSerializer