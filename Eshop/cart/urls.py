from django.urls import path 

from .views import AddToCart

from .views import view_cart, get_cart_item_count

from .views import update_quantity, remove_item

urlpatterns = [
    path('', view_cart, name = 'view_cart'),
    path('add/', AddToCart.as_view(), name = 'add_to_cart'),
     path('update-qty/', update_quantity, name='update_quantity'),
    path('remove-item/', remove_item, name='remove_item'),
    path('cart/count/', get_cart_item_count, name='cart_count'),
]