from django.shortcuts import render
from rest_framework import generics,permissions
from .models import Movie, Review, CustomUser
from .serializers import MovieSerializer, ReviewSerializer, CustomUserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view  # new
from rest_framework.response import Response  # new
from rest_framework import status
from rest_framework.reverse import reverse  # new
from .paginations import ReviewPagination
from rest_framework import filters
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django_filters.rest_framework import DjangoFilterBackend
from .models import ReviewFilter
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.postgres.search import SearchVector
from .filters import MovieFilter
from rest_framework.exceptions import PermissionDenied
# Create your views here.

# View for listing and creating movies
class MovieList(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MovieFilter
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter] 
    queryset = Movie.objects.all().order_by('title')
    ordering_fields = ['title', 'release_date', 'genre', 'id']  # Allow ordering by these fields
    ordering = ['title','id']
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.annotate(
                search=SearchVector('title', 'genre', 'release_date')
            ).filter(search=search_query)
        return queryset


    @swagger_auto_schema(
        operation_description="Retrieve a list of movies or create a new movie",
        responses={200: MovieSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new movie",
        request_body=MovieSerializer,
        responses={201: MovieSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


# View for retrieving, updating, and deleting a specific movie
class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_description="Retrieve, update or delete a movie",
        responses={200: MovieSerializer}
    )
    def get(self, request, pk, format=None):
        return super().get(request, pk, format)

    def put(self, request, pk, format=None):
        movie = get_object_or_404(Movie, pk=pk)
        # Allow users to update the genre of any movie
        if 'genre' in request.data:
            serializer = self.get_serializer(movie, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise PermissionDenied("You can only update the genre of the movie.")

    def perform_destroy(self, instance):
        # Only allow admin to delete movies
        if self.request.user.is_staff:
            instance.delete()
        else:
            raise PermissionDenied("You do not have permission to delete this movie.")

# View for listing and creating reviews
class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = ReviewPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter] 
    search_fields = ['movie__title']  # Searching in the related 'movie' field
    search_param = 'movie_title'
    filterset_fields = ['rating']  # Optional filtering by rating (1-5)
    filterset_class = ReviewFilter
    # Allowing ordering by rating or date_created

    # @swagger_auto_schema(
    #     operation_description="Retrieve a list of reviews or create a new review",
    #     responses={200: ReviewSerializer(many=True)}
    # )
    # def get(self, request, *args, **kwargs):
    #     return super().get(request, *args, **kwargs)

    # @swagger_auto_schema(
    #     operation_description="Create a new review",
    #     request_body=ReviewSerializer,
    #     responses={201: ReviewSerializer}
    # )




    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = Review.objects.all()  # Base queryset for all reviews
        
        # Extract query parameters
        movie_title = self.request.query_params.get('movie_title', None)
        rating = self.request.query_params.get('rating', None)

        # Filter by movie title if provided
        if movie_title:
            queryset = queryset.filter(movie__movie_title__icontains=movie_title)
        
        # Filter by rating if provided
        if rating:
            queryset = queryset.filter(rating=rating)
        
        return queryset
    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# View for retrieving, updating, and deleting a specific review
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_description="Retrieve, update or delete a review",
        responses={200: ReviewSerializer}
    )
    def get(self, request, pk, format=None):
        return super().get(request, pk, format)

    def put(self, request, pk, format=None):
        review = get_object_or_404(Review, pk=pk)
        # Check if the user is the author of the review
        if request.user != review.author:
            raise PermissionDenied("You did not submit this review go Back and create a review.")
        return super().put(request, pk, format)

    def perform_destroy(self, instance):
        # Check if the user is the author of the review or an admin
        if self.request.user == instance.author or self.request.user.is_staff:
            instance.delete()
        else:
            # Raise a permission denied error if the user is not authorized
            raise PermissionDenied("You do not have permission to delete this review.")

class MovieReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Allow only authenticated users to post reviews

    def post(self, request, *args, **kwargs):
        movie_id = self.kwargs.get('movie_id')
        movie = Movie.objects.get(id=movie_id)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can create reviews

    def post(self, request, *args, **kwargs):
        movie_id = self.kwargs.get('movie_id')  # Get the movie ID from the URL
        movie = get_object_or_404(Movie, id=movie_id)  # Get the movie or return 404 if not found

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(movie=movie, user=request.user)  # Save the review with the movie and user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserList(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class UserDetail(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


#single root API Endpoint
@api_view(["GET"]) 
def api_root(request, format=None):
    return Response(
        {
            "users": reverse("user-list", request=request, format=format),
            "reviews": reverse("reviews-list", request=request, format=format),
            "movies": reverse("movies-list", request=request, format=format),
        }
    )
