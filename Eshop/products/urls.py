from django.urls import path

from .views import productView, searchProducts

from .views import (
    CreateProduct, ProductDetail, UpdateProduct, DeleteProduct,ProductImageForm
)

from .views import (DeleteProductImage, EditProductImage)

urlpatterns=[
    path('all/',productView, name='product_page'),
    path('search/', searchProducts, name='search_products'),

    path('add/', CreateProduct.as_view(), name='add_product'),
    path('<int:pk>/', ProductDetail.as_view(), name='product_details'),
    path('<int:pk>/edit/', UpdateProduct.as_view(), name='edit_product'),
    path('<int:pk>/delete/', DeleteProduct.as_view(), name='delete_product'),

    path('<int:pk>/add/',ProductImageForm, name='add_product'),

    # Product Image
    path('image/edit/<int:pk>',EditProductImage.as_view(), name = 'edit_prod_image'),
    path('image/del/<int:pk>',DeleteProductImage.as_view(), name = 'del_prod_image'),

]
