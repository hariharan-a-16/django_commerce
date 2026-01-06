from django.urls import path

from . import views 


urlpatterns =[
    path('',views.homeView, name='home_page'),
    path("about/",views.aboutView, name='about_page'),
    path("contact/",views.contactView,name='contact_page')
]


