from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ListMovie, DetailMovie, MovieViewSet
from .views import MovieListView, MovieDetailView

#router setup
router = DefaultRouter()
router.register(r"movies", MovieViewSet, basename="movies")

# urlpatterns = router.urls

urlpatterns = [
    path("", ListMovie.as_view()),
    path("<int:pk>/", DetailMovie.as_view()),
    path('movies/', MovieListView.as_view()),
    path('movies/<int:pk>/', MovieDetailView.as_view()),
]