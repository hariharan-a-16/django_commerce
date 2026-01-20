from django.urls import path

from .views import productView, searchProducts

urlpatterns=[
    path('all/',productView, name='product_page'),
    path('search/', searchProducts, name='search_products')
]