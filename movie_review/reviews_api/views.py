from django.shortcuts import render
from rest_framework import generics
from .models import Movie, Review, User
from .serializers import MovieSerializer
# Create your views here.

class movieList(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class movieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

