from rest_framework import serializers
from movies.models import Movie, Review
from accounts.models import CustomUser
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']


class moviesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'created_at']

class ReviewSerializer(serializers.ModelSerializer):
    movie_title = serializers.ReadOnlyField(source='movie.movie_title')  # Display the movie title
    user = serializers.ReadOnlyField(source='user.username')  # Display the user name of the person creating the review

    class Meta:
        model = Review
        fields = ['id', 'movie', 'movie_title', 'review_content', 'rating', 'user', 'created_date']
        read_only_fields = ['user', 'created_date', 'title']