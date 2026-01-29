from django.shortcuts import render
from django.urls import reverse_lazy

# Using the built-in auth User model
from django.contrib.auth.models import User

# Extending the auth views
from django.contrib.auth.views import(
    LoginView
)

# CreateView CBV
from django.views.generic import CreateView


# Create your views here.

class UserRegisterView(CreateView):
    model = User
    fields = ['username','password']
    template_name = 'authentication/register.html'
    success_url = reverse_lazy('signin')

class UserLoginView(LoginView):
    template_name = 'authentication/login.html'

