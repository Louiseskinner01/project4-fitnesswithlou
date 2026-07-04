import stripe
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from cart.models import Cart
from cart.contexts import cart_contents


from users.models import UserProfile
from products.models import Product

from .forms import OrderForm
from .models import Order, OrderLineItem

import json


@csrf_exempt
def stripe_webhook(request):
    """
    Handle incoming Stripe webhook events.
    The @csrf_exempt decorator is required because Stripe sends
    webhook POST requests without a Django CSRF token.
    Validates the webhook signature to ensure the request
    genuinely came from Stripe before processing.
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        # Verify the webhook signature using the Stripe signing secret
        # This prevents malicious actors from sending fake webhook events
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WH_SECRET
        )
    except ValueError:
        # Invalid payload — return 400 Bad Request
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature — return 400 Bad Request
        return HttpResponse(status=400)

    # Handle successful payment intent
    if event['type'] == 'payment_intent.succeeded':
        intent = event['data']['object']
        print("Webhook received payment success:", intent.id)

    return HttpResponse(status=200)


@login_required
def checkout(request):
    """
    Handle the checkout process for product purchases.
    GET request: Creates a Stripe PaymentIntent and renders
    the checkout page with the order form pre-filled with
    the user's saved profile information.
    POST request: Validates and saves the order form, creates
    the order and line items in the database, then redirects
    to the checkout success page.
    """
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Retrieve the user's current cart from the database
    cart = Cart.objects.filter(user=request.user).first()
    
    # Redirect to products if cart is empty or doesn't exist
    if not cart or not cart.items.exists():
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products:products'))

    cart_items = cart.items.all()

    # Calculate the order total from cart items
    total = sum(item.product.price * item.quantity for item in cart_items)

    # ------------------------
    # POST request = process the submitted checkout form
    # ------------------------
    if request.method == "POST":
        # Check if user wants to save delivery info to their profile
        save_info = 'save_info' in request.POST
        request.session['save_info'] = save_info

        order_form = OrderForm(request.POST)

        if order_form.is_valid():
            # Save the order without committing to database yet
            # so we can add additional fields first
            order = order_form.save(commit=False)
            order.user = request.user

            # Extract the PaymentIntent ID from the client secret
            # The client secret format is: pi_xxx_secret_xxx
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid

            # Store the bag contents as JSON for webhook reference
            order.original_bag = json.dumps({
                str(item.product.id): item.quantity
                for item in cart_items
            })
            print(f" ORDER SAVED - PID: {order.stripe_pid}")
            order.save()

            # Create an order line item for each product in the cart
            for item in cart_items:
                print("SIZE DEBUG:", item.size)

                OrderLineItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    product_size=item.size
                )

            # Recalculate and save the order total including delivery
            order.update_total()

             # Redirect to success page with the order summary
            return redirect('checkout:checkout_success', order.order_number)
    else:
        messages.error(request, "There was an issue with your order.")

        # ------------------------
        # GET request = load the checkout page
        # ------------------------
        
        # Convert total to pence/cents as Stripe requires integer amounts
        stripe_total = int(total * 100)

        # Create a Stripe PaymentIntent with the order amount
        # Metadata is attached to link the payment to the cart contents
        # and user information for webhook processing
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
            automatic_payment_methods={
                'enabled': True,
            },
            metadata={
                # Store bag contents so webhook can recreate order if needed
                'bag': json.dumps({
                    str(item.product.id): item.quantity
                    for item in cart_items
                }),
                'save_info': 'False',
                'username': request.user.username,
            }
        )

    # Pre-fill the order form with the user's saved profile information
    try:
        profile = UserProfile.objects.get(user=request.user)

        order_form = OrderForm(initial={
            'email': request.user.email,
            'phone_number': profile.default_phone_number,
            'street_address1': profile.default_street_address1,
            'street_address2': profile.default_street_address2,
            'town_or_city': profile.default_town_or_city,
            'postcode': profile.default_postcode,
            'country': profile.default_country,
        })

    except UserProfile.DoesNotExist:
        # No profile found — render empty order form
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
    """
    Handle successful checkout completion.
    Retrieves the completed order, optionally saves delivery
    information to the user's profile if save_info was checked,
    clears the user's cart, and renders the success page.
    """

    # Retrieve the completed order using the unique order number
    order = get_object_or_404(Order, order_number=order_number)
    
    # Check if the user requested to save their delivery information
    save_info = request.session.get('save_info')

    print(request.session.get('save_info'))
    if save_info:
        # Update the user's profile with the delivery details
        # used in this order for future checkouts
        profile = UserProfile.objects.get(user=request.user)

        profile.default_phone_number = order.phone_number
        profile.default_street_address1 = order.street_address1
        profile.default_street_address2 = order.street_address2
        profile.default_town_or_city = order.town_or_city
        profile.default_postcode = order.postcode
        profile.default_country = order.country

        profile.save()

    # Clear the user's cart after successful checkout
    # so it's empty for their next visit
    cart = Cart.objects.filter(user=request.user).first()

    if cart:
        cart.items.all().delete()

    context = {
        'order': order,
    }

    return render(request, 'checkout/success.html', context)
