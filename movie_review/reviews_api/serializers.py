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
        fields = ['id','title']  # Fields I will be showing

# Serializer for Review
class ReviewSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)  # Display user info in GET requests
    movie = MovieSerializer(read_only=True)  # Display movie info in GET requests
    movie_id = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all(), source='movie', write_only=True)
    
    # For POST requests, accept user_id and movie_id
    user_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), source='user', write_only=True, required=False)

    class Meta:
        model = Review
        fields = ['id', 'author', 'user', 'user_id', 'review_date', 'stars', 'comment', 'movie', 'movie_id']

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