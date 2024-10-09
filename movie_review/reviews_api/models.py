from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils import timezone
from django.conf import settings
from accounts.models import CustomUser
# Create your models here.




class Movie(models.Model):
    title = models.CharField(max_length=40)
    movie_type = models.CharField(max_length=20, default="Action")
    description =  models.TextField(max_length=3000)
    title_upload_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    



class Review(models.Model):
    author = models.CharField(max_length=40, blank=True, null=True, default="anonymous")
    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL)  # Use CustomUser
    review_date = models.DateTimeField(default=timezone.now)
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

    def __str__(self):
        if self.user:
            return f"{self.user.username}'s review of {self.movie.title}"
        return f"{self.author}'s review of {self.movie.title}"