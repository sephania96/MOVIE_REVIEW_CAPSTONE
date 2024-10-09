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

# Create your views here.


class MovieList(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # new

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = ReviewPagination

    # Adding the search and filtering backends
    filter_backends = [filters.SearchFilter]
    
    # Allowing searching by movie title
    search_fields = ['movie__title']  # Searching in the related 'movie' field
    search_param = 'movie_title'
    
    # Allowing filtering by rating
    filterset_fields = ['rating']  # Optional filtering by rating (1-5)
    
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


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]  # Consider adding custom permissions

    def get_object(self, pk):
        try:
            return Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        review = self.get_object(pk)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        review = self.get_object(pk)
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        review = self.get_object(pk)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
