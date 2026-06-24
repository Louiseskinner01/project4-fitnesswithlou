from decimal import Decimal
from django.conf import settings
from .models import Cart

def cart_contents(request):

    cart_items = []
    total = 0
    product_count = 0
    cart = None
    delivery = 0
    free_delivery_delta = 0

    try:
        if hasattr(request, 'user') and request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()

        if cart:
            for item in cart.items.all():
                product = item.product
                quantity = item.quantity
                total += product.price * quantity
                product_count += quantity
                cart_items.append({
                    'id': item.id,
                    'product': item.product,
                    'quantity': item.quantity,
                    'price': product.price,
                    'size': item.size,
                })

        if total < settings.FREE_DELIVERY_ABOVE:
            delivery = total * Decimal(settings.DELIVERY_PERCENTAGE / 100)
            free_delivery_delta = settings.FREE_DELIVERY_ABOVE - total
        else:
            delivery = 0
            free_delivery_delta = 0

    except Exception:
        pass

    grand_total = delivery + total

    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_ABOVE,
        'grand_total': grand_total,
    }

    return context