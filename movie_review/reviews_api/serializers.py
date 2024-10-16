from rest_framework import serializers
from .models import Movie, Review
from django.conf import settings
from accounts.models import CustomUser 
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import PrimaryKeyRelatedField


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser  # Reference your CustomUser model
        fields = ['username']  # changed to only show the username of the user 

# Serializer for Movie
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id','title','genre','release_date']  # Fields I will be showing
        

# Serializer for Review
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username') # Display the user name of the person creating the review
    movie = serializers.ReadOnlyField(source='movie.title') # Display the movie title

    def perform_create(self, serializer):
        # Automatically associate the review with the logged-in user and validate the movie exists
        movie_id = self.request.data.get('movie')  # Get the movie ID from request
        try:
            movie = Movie.objects.get(id=movie_id)
            # Set the user who created the review as the logged-in user
            serializer.save(user=self.request.user, movie=movie)
        except Movie.DoesNotExist:
            raise Response({"error": "Movie does not exist."}, status=status.HTTP_400_BAD_REQUEST)
    

    class Meta:
        model = Review
        fields = ['id', 'author', 'user','review_date', 'stars', 'comment','movie']
        read_only_fields = ['user']
        # fields = ['id', 'author', 'user', 'user_id','review_date', 'stars', 'comment', 'movie', 'movie_id']

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().update(instance, validated_data)
    