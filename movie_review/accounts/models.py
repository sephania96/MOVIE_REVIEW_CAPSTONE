from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser, BaseUserManager
class UserManager(BaseUserManager):
    def create_user(self, email, username, password):
        if not email:
            raise ValueError("Email is required")
        user = self.model(email=self.normalize_email(email), username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, username, password):
        user = self.create_user(email=email, username=username, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
class CustomUser(AbstractUser):
    email = models.CharField(max_length=255, unique=True)
    username = models.CharField(unique=False, max_length=15)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    # add additional fields in here

    def __str__(self):
        return self.username
    

#my profile model
    
class Users(models.Model):
    pic  = models.ImageField(upload_to='profile_pics', blank=True)
    bio = models.TextField(max_length=500, blank=True)
    country = models.CharField(max_length=100, default='Unknown')
    review_by = models.ForeignKey(CustomUser , on_delete=models.CASCADE, related_name='users', null=True)
    
    # review_by = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)