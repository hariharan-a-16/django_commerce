from django.urls import path

from .views import UserRegisterView,UserLoginView

# Password reset
from .views import send_otp_mail


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name ='signup'),
    path('login/', UserLoginView.as_view(), name='signin'),

    path('send_otp/', send_otp_mail, name='send_otp')
]