from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Movie
from datetime import date

class MovieListViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('movies-list')

        # Clear any existing data (if needed)
        Movie.objects.all().delete()

        # Create exactly 2 movies
        Movie.objects.create(title='Movie 1', genre='Action', release_date=date(2022, 1, 1))
        Movie.objects.create(title='Movie 2', genre='Comedy', release_date=date(2023, 2, 2))

    def test_get_movie_list(self):
        response = self.client.get(self.url)
        print("Movies in test database:", list(Movie.objects.all()))
        print("Response data:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)