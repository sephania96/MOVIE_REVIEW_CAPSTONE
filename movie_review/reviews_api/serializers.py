from rest_framework import serializers
from .models import Movie, Review
from django.conf import settings
from accounts.models import CustomUser 


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser  # Reference your CustomUser model
        fields = ['id', 'username', 'email']  # Add more fields if necessary (e.g., profile data)

# Serializer for Movie
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'title_upload_date']  # Fields you want to expose

# Serializer for Review
class ReviewSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)  # Nested serializer for my user details
    movie = MovieSerializer(read_only=True)  # Optionally, you can nest the Movie serializer too

    class Meta:
        model = Review
        fields = ['id', 'author', 'user', 'review_date', 'stars', 'comment', 'movie']