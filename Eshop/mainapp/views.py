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





from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from .models import CarouselImage

class CarouselImageListView(ListView):
    model = CarouselImage
    template_name = 'mainapp/carousel_list.html'
    context_object_name = 'images'

class CarouselImageCreateView(CreateView):
    model = CarouselImage
    fields = '__all__'
    template_name = 'mainapp/carousel_form.html'
    success_url = reverse_lazy('carousel_list')

class CarouselImageUpdateView(UpdateView):
    model = CarouselImage
    fields = '__all__'
    template_name = 'mainapp/carousel_form.html'
    success_url = reverse_lazy('carousel_list')

class CarouselImageDeleteView(DeleteView):
    model = CarouselImage
    template_name = 'mainapp/carousel_delete.html'
    success_url = reverse_lazy('carousel_list')



    

    