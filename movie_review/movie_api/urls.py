from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import moviesListCreateAPIview, moviesRetrieveUpdateDestroy



urlpatterns = [
    path("movies/", moviesListCreateAPIview.as_view(), name="movies-list-create"),
    path("movies/<int:pk>/", moviesRetrieveUpdateDestroy.as_view(), name="movies-retrieve-update-destroy"),
]
















#router setup
# router = DefaultRouter()
# router.register(r"movies", MovieViewSet, basename="movies")

# urlpatterns = router.urls

# urlpatterns = [
#     path("", include(router.urls)),
# ]