# yourapp/management/commands/fetch_movies.py
import requests
from django.core.management.base import BaseCommand
from reviews_api.models import Movie
from datetime import datetime

class Command(BaseCommand):
    help = 'Fetch movies from TMDb API'

    def handle(self, *args, **kwargs):
        api_key = 'api-key'
        url = 'https://api.themoviedb.org/3/search/movie'

        # Define your search parameters
        params = {
            'api_key': api_key,
            'query': 'Mummy',  # Example movie title
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

                    # Fetch detailed movie information to get genres
                    movie_id = movie_data['id']
                    genre = self.get_movie_genre(api_key, movie_id)

                    movie, created = Movie.objects.get_or_create(
                        title=movie_data['title'],
                        defaults={
                            'genre': genre,
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
            self.stdout.write(response.text)

    def get_movie_genre(self, api_key, movie_id):
        """Fetch the genre of a movie using its ID."""
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US'
        response = requests.get(url)
        
        if response.status_code == 200:
            movie_details = response.json()
            genres = [genre['name'] for genre in movie_details.get('genres', [])]
            return ', '.join(genres)  # Return genres as a comma-separated string
        else:
            self.stdout.write(self.style.ERROR(f'Failed to fetch genre for movie ID {movie_id}: {response.status_code}'))
            return "Unknown"