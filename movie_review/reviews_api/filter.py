import requests

API_KEY = 'your_api_key'  # Replace with your actual API key
BASE_URL = 'https://api.themoviedb.org/3'

def fetch_movies():
    url = f"{BASE_URL}/movie/popular?api_key={API_KEY}&language=en-US&page=1"
    response = requests.get(url)
    
    if response.status_code == 200:
        movies_data = response.json()
        movies = []
        
        for movie in movies_data['results']:
            movie_details = {
                'title': movie['title'],
                'release_date': movie['release_date'],
                'genre': get_movie_genres(movie['id']),  # Fetch genre using movie ID
            }
            movies.append(movie_details)
        
        return movies
    else:
        print("Failed to fetch movies:", response.status_code)
        return []

def get_movie_genres(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    
    if response.status_code == 200:
        movie_details = response.json()
        genres = [genre['name'] for genre in movie_details.get('genres', [])]
        return ', '.join(genres)  # Return genres as a comma-separated string
    else:
        print("Failed to fetch movie genres:", response.status_code)
        return "Unknown"