from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cart.models import Cart
from .forms import OrderForm
import stripe
from django.conf import settings
from cart.contexts import cart_contents


@login_required
def checkout(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    cart = Cart.objects.filter(user=request.user).first()
    if not cart or not cart.items.exists():
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products:products'))
    
    cart_items = cart.items.all()
    total = sum(item.product.price * item.quantity for item in cart_items)

    stripe_total = int(total * 100)

    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
        # automatic_payment_methods={
        # 'enabled': True,
        # },
         payment_method_types=['card'],
    )

    order_form = OrderForm()

    context = {
        'order_form': order_form,
        'cart_items': cart_items,
        'total': total,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'client_secret': intent.client_secret,
    }

    return render(request, 'checkout/checkout.html', context) 

    