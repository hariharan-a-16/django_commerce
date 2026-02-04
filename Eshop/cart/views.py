from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.urls import reverse

from django.contrib.auth.decorators import login_required

from .models import CartItem
from products.models import Product


class AddToCart(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                'error': 'login_required',
                'redirect_url': reverse('signin')
            }, status=401)

        product_id = request.POST.get('product_id')
        this_product = get_object_or_404(Product, id=product_id)

        item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=this_product
        )
        item.quantity += 1
        item.save()

        cart_count = CartItem.objects.filter(user=request.user).count()

        return JsonResponse({
            'message': f'{this_product.title.capitalize()} was added to cart',
            'cart_count': cart_count
        })


@login_required
def view_cart(request):
    items = CartItem.objects.filter(user=request.user)

    total_price = 0
    for item in items:
        total_price += float(item.product.price) * item.quantity

    grand_total = total_price

    return render(request, "cart/cart.html", {
        "cart_items": items,
        "total_price": total_price,
        "grand_total": grand_total,
    })


def get_cart_item_count(request):
    return JsonResponse({
        'cart_count': CartItem.objects.filter(user=request.user).count()
    })
