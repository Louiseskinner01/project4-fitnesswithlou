from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cart.models import Cart
from .forms import OrderForm

@login_required
def checkout(request):
 
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or not cart.items.exists():
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products:products'))
    
    order_form = OrderForm()

    cart_items = cart.items.all()
    total = sum(item.product.price * item.quantity for item in cart_items)

    context = {
        'order_form': order_form,
        'cart_items': cart_items,
        'total': total,
    }

    return render(request, 'checkout/checkout.html', context)