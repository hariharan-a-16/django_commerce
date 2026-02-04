from django.shortcuts import render, redirect
from django.urls import reverse_lazy

# Using the built-in auth User model
from django.contrib.auth.models import User

# Extending the auth views
from django.contrib.auth.views import(
    LoginView
)

# CreateView CBV
from django.views.generic import CreateView
from .forms import UserRegisterForm, UserLoginForm

# Create your views here.

class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'authentication/register.html'
    success_url = reverse_lazy('signin')

class UserLoginView(LoginView):
    template_name = 'authentication/login.html'
    authentication_form = UserLoginForm

# Password Reset Flow

import random
from django.core.mail import send_mail
from django.conf import settings
from .models import EmailOTP

def generate_otp():
    return str(random.randint(100000,999999))

def send_otp_mail(request):
    context = None
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            otp = generate_otp()
            EmailOTP.objects.create(email = email, otp = otp)

            #  Prepare the email
            subject = "Your OTP Code"
            message = f"Your OTP is {otp}. It will expire in 10 minutes"
            send_mail(
                subject = subject,
                message = message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list = [email],
                fail_silently=False
            
            )

            request.session['email_for_reset'] = email
            return redirect('verify_otp')
        context = {
                'error' : "Email Missing"
            }
    if not context:
            context = {}
    return render(request, template_name='authentication/pwd_reset/send_otp_email.html',
                      context=context)
    