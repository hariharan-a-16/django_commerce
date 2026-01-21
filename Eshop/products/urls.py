from django.urls import path

from .views import productView, searchProducts

from .views import (
    CreateProduct, ProductDetail, UpdateProduct, DeleteProduct
)

urlpatterns=[
    path('all/',productView, name='product_page'),
    path('search/', searchProducts, name='search_products'),

    path('add/', CreateProduct.as_view(), name='add_product'),
    path('<int:pk>/', ProductDetail.as_view(), name='product_details'),
    path('<int:pk>/edit/', UpdateProduct.as_view(), name='edit_product'),
    path('<int:pk>/delete/', DeleteProduct.as_view(), name='delete_product')

]
