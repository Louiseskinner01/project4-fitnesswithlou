from decimal import Decimal
from django.conf import settings
from .models import Cart


def cart_contents(request):
    """
    Context processor that makes cart data available to all templates.
    This function is registered in settings.py under TEMPLATES context
    processors, meaning it runs on every request and injects cart
    information into every template automatically.
    Calculates cart totals, delivery costs and the free delivery delta
    (how much more the user needs to spend to qualify for free delivery).
    Wrapped in a try/except to prevent cart errors from causing 500
    errors on 404 pages where the request context may not be fully
    initialised.
    """

    # Initialise default values for all context variables
    cart_items = []
    total = 0
    product_count = 0
    cart = None
    delivery = 0
    free_delivery_delta = 0

    try:
        # Only attempt to retrieve the cart if the request has a user
        # and that user is authenticated — avoids errors on 404 pages
        # where the request object may not be fully initialised
        if hasattr(request, 'user') and request.user.is_authenticated:
            # Get the first cart belonging to this user
            # Returns None if no cart exists
            cart = Cart.objects.filter(user=request.user).first()

        if cart:
            # Loop through all items in the cart and calculate totals
            for item in cart.items.all():
                product = item.product
                quantity = item.quantity

                # Add item total to the running cart total
                total += product.price * quantity

                # Count total number of items in the cart
                product_count += quantity

                # Add item details to the cart_items list
                # for use in templates
                cart_items.append({
                    'id': item.id,
                    'product': item.product,
                    'quantity': item.quantity,
                    'price': product.price,
                    'size': item.size,
                })

        # Calculate delivery cost based on order total
        if total < settings.FREE_DELIVERY_ABOVE:
            # Apply delivery charge as a percentage of the order total
            delivery = total * Decimal(settings.DELIVERY_PERCENTAGE / 100)
            # Calculate how much more the user needs to spend
            # to qualify for free delivery
            free_delivery_delta = settings.FREE_DELIVERY_ABOVE - total
        else:
            # Order total meets or exceeds free delivery threshold
            delivery = 0
            free_delivery_delta = 0

    except Exception:
        # Silently catch any exceptions to prevent the context processor
        # from causing 500 errors on pages like 404 where the full
        # request context may not be available
        pass

    # Calculate the final grand total including delivery
    grand_total = delivery + total

    # Return all cart data as a dictionary available to every template
    context = {
        'cart_items': cart_items,        # List of cart item dictionaries
        'total': total,                  # Cart subtotal before delivery
        'product_count': product_count,  # Total number of items in cart
        'delivery': delivery,            # Delivery cost
        'free_delivery_delta': free_delivery_delta,  # Amount needed for free delivery
        'free_delivery_threshold': settings.FREE_DELIVERY_ABOVE,  # Free delivery threshold
        'grand_total': grand_total,      # Final total including delivery
    }

    return context