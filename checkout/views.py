from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from cart.models import Cart
from cart.contexts import cart_contents
from .forms import OrderForm
from .models import Order, OrderLineItem
import stripe




@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WH_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    # Handle successful payment
    if event['type'] == 'payment_intent.succeeded':
        intent = event['data']['object']
        print("Webhook received payment success:", intent.id)

    return HttpResponse(status=200)

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

            for item in cart_items:
                OrderLineItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity
        )

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