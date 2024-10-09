from django.urls import path, include
from reviews_api import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("movies/", views.MovieList.as_view()),
    path("movies/<int:pk>/", views.MovieDetail.as_view()),
    path("reviews/", views.ReviewList.as_view()),
    path("reviews/<int:pk>/", views.ReviewDetail.as_view()),
    path("users/", views.UserList.as_view()),
    path("users/<int:pk>/", views.UserDetail.as_view()),
]

#This is to allow the API to accept different formats
urlpatterns = format_suffix_patterns(urlpatterns)