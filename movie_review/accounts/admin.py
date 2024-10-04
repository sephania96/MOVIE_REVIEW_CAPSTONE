from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username",] #below is an additional features i added . im yet to use
    search_fields = ["email", "username"]
    filter_horizontal = ["groups", "user_permissions"]

admin.site.register(CustomUser, CustomUserAdmin)

# this below code is to manage profile of each user that is registered

from .models import Users

class ProfileAdmin(admin.ModelAdmin):
    list_display = ["review_by", "bio", "country"]
    search_fields = ["review_by__email", "review_by__username"]

admin.site.register(Users, ProfileAdmin)