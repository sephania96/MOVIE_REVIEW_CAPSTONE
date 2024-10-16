from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils import timezone
from django.conf import settings
from accounts.models import CustomUser
import django_filters
# Create your models here.




class Movie(models.Model):
    title = models.CharField(max_length=40)
    genre = models.CharField(max_length=255, blank=False, null=True, default="Action")
    release_date = models.DateField(blank=True, null=True)
    # movie_type = models.CharField(max_length=20, default="Action")
    # description =  models.TextField(max_length=3000)
    # title_upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    



class Review(models.Model):
    author = models.CharField(max_length=40, blank=True, null=True, default="anonymous")
    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL)  # Use CustomUser
    review_date = models.DateTimeField(auto_now_add=True)
    rate_choices = (
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5)
    )
    stars = models.IntegerField(choices=rate_choices)
    comment = models.TextField(max_length=4000)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

class ReviewFilter(django_filters.FilterSet):
    # Assuming 'rating' is a field on a related 'Movie' model
    rating = django_filters.NumberFilter(field_name='movie__rating')

    class Meta:
        model = Review
        
        fields = [] 

    def __str__(self):
        if self.user:
            return f"{self.user.username}'s review of {self.movie.title}"
        return f"{self.author}'s review of {self.movie.title}"