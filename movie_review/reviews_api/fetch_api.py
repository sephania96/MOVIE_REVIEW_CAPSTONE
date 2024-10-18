import requests
from django.conf import settings
import logging


# Set up logging
logger = logging.getLogger(__name__)

def fetch_movies_from_api():
    # url = "https://api.themoviedb.org/3/movie/popular"
    url = f'https://api.themoviedb.org/3/movie/upcoming?api_key={'426e0f0d6d436de1adbe6273d455a8eb'}&language=en-US&page=1'
    params = {
        '426e0f0d6d436de1adbe6273d455a8eb': settings.TMDB_API_KEY,
        'language': 'en-US',
        'page': 1
    }
    
    response = requests.get(url, params=params)
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        
        return response.json().get('results', [])
    
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")  # Log the error
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request error occurred: {req_err}")  # Log the error
    except Exception as e:
        logger.error(f"An error occurred: {e}")  # Log any other errors
    
    return []  # Return an empty list if there was an error