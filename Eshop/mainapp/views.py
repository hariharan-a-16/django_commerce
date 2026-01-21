from django.shortcuts import render
from .models import CarouselImage
from products.models import Product

# Create your views here.

def homeView(request):
    template = 'mainapp/home.html'
    context = {

        'current_page' : 'home',

        #Let's collect all existing records of carousel image table to be sent yo template
        'carousel_images' : CarouselImage.objects.all(), # Select * from carousel_image;
         'products' : Product.objects.all() # show all product card on home page
    }

    return render(request, template_name= template, context= context)



def aboutView(request):
    template = 'mainapp/about.html'
    context = { 
        'current_page' :'about'
    }

    return render(request, template_name= template, context= context)


def contactView(request):
    template = 'mainapp/contact.html'
    context = {
        'current_page' : 'contact'
    }

    return render(request, template_name= template, context= context)



    

    