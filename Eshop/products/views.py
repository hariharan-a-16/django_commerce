from django.shortcuts import render, redirect # redirct is used for after upload to the ne next page
from django.urls import reverse # it work came the same product page
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
    else:
        context = {
            'query' : query,
            'products' : None
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

    
from django.views.generic.edit import FormMixin
 # This mixin provides ability to render forms from the `form_class`
from .forms import ProductImageForm


class ProductDetail(FormMixin, DetailView):
    model = Product
    template_name = 'product/product_details.html'  
    context_object_name = 'product'
    # providing form class for Product Image
    form_class = ProductImageForm

    def get_success_url(self):
        return reverse('product_details', kwargs={'pk' :self.object.pk})

  #Overriding the the querset to pre-fetch
  # and add the product images alongside products
    def get_queryset(self):
        return Product.objects.prefetch_related('images')
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            image = form.save(commit = False)
            image.product = self.object
            image.save()

            return redirect(self.get_success_url())
        


class UpdateProduct(UpdateView):
    model = Product
    template_name = 'product/update_product.html'
    fields='__all__'
    success_url = '/'


class DeleteProduct(DeleteView):
    model = Product
    template_name = 'product/delete_product.html'
    success_url = '/'

# Edit Product Image
from .models import ProductImage

class EditProductImage(UpdateView):
    model = ProductImage
    template_name = 'product/image_edit.html'
    fields = '__all__'


    def get_success_url(self):
        return reverse('product_details', kwargs={'pk':self.object.product.pk})
    
class DeleteProductImage(DeleteView):
    model = ProductImage
    template_name = 'product/image_del.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('product_details', kwargs={'pk':self.object.product.pk}) 
    
# For Product detail add carousel image

from django.shortcuts import get_object_or_404, redirect
from .models import Product, ProductImage
from .forms import ProductImageForm

def AddImages(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductImageForm(request.POST, request.FILES)
        if form.is_valid():
            media = form.save(commit=False)
            media.product = product
            media.save()
            return redirect('product_details', pk=pk)
    else:
        form = ProductImageForm()

    return render(
        request,
        'product/includes/add_image_carousel.html',
        {
            'form': form,
            'product': product
        }
    )