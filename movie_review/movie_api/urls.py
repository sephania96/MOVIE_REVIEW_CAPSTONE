from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from .views import MovieViewSet
from .views import moviesListCreateAPIview, moviesRetrieveUpdateDestroy, MovieViewSet
from .views import MovieListView, MovieDetailView

#router setup
# router = DefaultRouter()
# router.register(r"movies", MovieViewSet, basename="movies")

# urlpatterns = router.urls

urlpatterns = [
    path("", moviesListCreateAPIview.as_view()),
    path("<int:pk>/", moviesRetrieveUpdateDestroy.as_view()),
    # path('movies/', MovieListView.as_view()),
    # path('movies/<int:pk>/', MovieDetailView.as_view()),
]

# urlpatterns = [
#     path("", include(router.urls)),
# ]