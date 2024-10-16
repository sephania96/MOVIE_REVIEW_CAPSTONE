from django.urls import path, include
from reviews_api import views
from rest_framework.urlpatterns import format_suffix_patterns
from .views import MovieReviewCreateView,ReviewCreateView

urlpatterns = [
    path("movies/", views.MovieList.as_view(),name="movies-list"),
    path("movies/<int:pk>/", views.MovieDetail.as_view()),
    path("reviews/", views.ReviewList.as_view(),name="reviews-list"),
    path("reviews/<int:pk>/", views.ReviewDetail.as_view()),
    path("users/", views.UserList.as_view(),name="user-list"),
    path("users/<int:pk>/", views.UserDetail.as_view()),
    path('movies/<int:movie_id>/reviews/', MovieReviewCreateView.as_view(), name='movie-review-create'),
    path('movies/<int:movie_id>/reviews/', ReviewCreateView.as_view(), name='review-create'),
    # path('movies/<int:movie_id>/reviews/', MovieReviewListView.as_view(), name='movie-reviews-list'),
    path("", views.api_root),
]

#This is to allow the API to accept different formats
urlpatterns = format_suffix_patterns(urlpatterns)