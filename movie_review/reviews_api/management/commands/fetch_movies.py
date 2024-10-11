# yourapp/management/commands/fetch_movies.py
import requests
from django.core.management.base import BaseCommand
from reviews_api.models import Movie
from datetime import datetime

class Command(BaseCommand):
    help = 'Fetch movies from TMDb API'

    def handle(self, *args, **kwargs):
        api_key = '12'
        url = 'https://api.themoviedb.org/3/search/movie'

        # Define your search parameters
        params = {
            'api_key': api_key,
            'query': 'Interstellar',  # Example movie title
            'language': 'en-US',
            'page': 1,
            'include_adult': False
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'results' in data:
                for movie_data in data['results']:
                    release_date_str = movie_data.get('release_date', None)
                    release_date = None

                    # Convert release_date_str to a datetime object if it's valid
                    if release_date_str:
                        try:
                            release_date = datetime.strptime(release_date_str, '%Y-%m-%d').date()
                        except ValueError:
                            self.stdout.write(self.style.WARNING(f"Invalid date format for movie: {movie_data['title']}"))

                    movie, created = Movie.objects.get_or_create(
                        title=movie_data['title'],
                        defaults={
                            'genre': ', '.join(genre['name'] for genre in movie_data.get('genres', [])),
                            'release_date': release_date,
                        }
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Added movie: {movie.title}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Movie already exists: {movie.title}'))
            else:
                self.stdout.write(self.style.ERROR('No movies found'))
        else:
            self.stdout.write(self.style.ERROR(f'Failed to fetch data from TMDb API: {response.status_code}'))
            self.stdout.write(response.text)  # Print the response text for more details