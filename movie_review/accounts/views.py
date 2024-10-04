from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
# Create your views here.


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

#below is mu alteration for my webpages
# from django.shortcuts import render
# from movies.models import movies as Project

# def project_index(request):
#     projects = Project.objects.all()
#     context = {
#         "projects": projects
#     }
#     return render(request, "home.html", context)