from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cart.models import Cart
from .forms import OrderForm
import stripe
from django.conf import settings
from cart.contexts import cart_contents
from .models import Order
from django.shortcuts import get_object_or_404



@login_required
def checkout(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    cart = Cart.objects.filter(user=request.user).first()

    if not cart or not cart.items.exists():
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products:products'))

    cart_items = cart.items.all()
    total = sum(item.product.price * item.quantity for item in cart_items)

    # ------------------------
    # POST = after Stripe payment
    # ------------------------
    if request.method == "POST":

        order_form = OrderForm(request.POST)

        if order_form.is_valid():
            order = order_form.save()

            return redirect('checkout:checkout_success', order.order_number)

        else:
            messages.error(request, "There was an issue with your order.")

    # ------------------------
    # GET = load checkout page
    # ------------------------
    stripe_total = int(total * 100)

    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
        automatic_payment_methods={
            'enabled': True,
        },
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


@login_required
def checkout_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    context = {
        'order': order,
    }

    return render(request, 'checkout/success.html', context)