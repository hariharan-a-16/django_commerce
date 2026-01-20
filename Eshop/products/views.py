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