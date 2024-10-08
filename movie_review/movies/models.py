from django.db import models
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import CustomUser
# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)  # Movie relationship
    review_content = models.TextField()  
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    created_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['created_date']
    def __str__(self):
        return self.title