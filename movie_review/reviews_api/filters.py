import django_filters
from .models import Movie

class MovieFilter(django_filters.FilterSet):
    class Meta:
        model = Movie
        fields = {
            'title': ['exact', 'icontains'],  # Allows exact match and case-insensitive contains
            'genre': ['exact'],
            'release_date': ['exact', 'year__gt'],  # Example of filtering by year
        }

