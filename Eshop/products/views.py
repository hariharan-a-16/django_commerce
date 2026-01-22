from django.shortcuts import render

from .models import Product
# Create your views here.

def productView(request):
    template= 'product/product.html'
    context={
        'current_page' : 'product',
        'products' : Product.objects.all()
    }

    return render(request, template_name=template, context=context)



# search Products
from django.db.models import Q
def searchProducts(request):
    template = 'product/search_results.html'
    query = request.GET.get('q')
    if query:
        search_results = Product.objects.filter(
            Q(title__icontains = query) |
            Q(desc__icontains = query)

        )

        context ={
            'query' : query,
            'products' : search_results
        }
    return render(request, template_name=template, context = context)


    # CRUD operations using Generic Class Based Viwes of Django

from django.views.generic import (CreateView, DetailView,
                                 UpdateView,DeleteView)

# ListView has already been implemented using a function above: productView()

class CreateProduct(CreateView):
    model = Product
    template_name = 'product/add_product.html'
    fields = '__all__'
    # redirection url for successful creation of resource
    success_url = '/'

class ProductDetail(DetailView):
    model = Product
    template_name = 'product/product_details.html'  
    context_object_name = 'product'

  #Overriding the the querset to pre-fetch
  # and add the product images alongside products
    def get_queryset(self):
        return Product.objects.prefetch_related('images')

class UpdateProduct(UpdateView):
    model = Product
    template_name = 'product/update_product.html'
    fields='__all__'
    success_url = '/'

class DeleteProduct(DeleteView):
    model = Product
    template_name = 'product/delete_product.html'
    success_url = '/'

