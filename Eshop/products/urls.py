from django.urls import path

from . import views 

urlpatterns=[
    path("",views.productView, name='product_page')
]