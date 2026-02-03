from django.urls import path 

from .views import AddToCart

from .views import view_cart

urlpatterns = [
    path('', view_cart, name = 'view_cart'),
    path('add/', AddToCart.as_view(), name = 'add_to_cart')
]