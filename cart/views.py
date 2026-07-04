from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from products.models import Product
from django.contrib import messages


@login_required
def view_cart(request):
    """
    Display the user's shopping cart.
    Retrieves or creates a cart for the authenticated user
    and renders all cart items in the shopping cart template.
    The @login_required decorator ensures only authenticated
    users can access the cart.
    """
    # Get the user's cart or create one if it doesn't exist yet
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Pass the cart and its items to the template
    context = {
        'cart': cart,
        'items': cart.items.all()
    }

    return render(request, 'cart/shopping_cart.html', context)


@login_required
def add_to_cart(request, product_id):
    """
    Add a product to the user's cart or increase its quantity.
    Retrieves the product by ID, gets the requested quantity
    and size from the POST request, then either creates a new
    cart item or increments the quantity if the item already
    exists in the cart.
    Redirects to the URL specified in the POST data or falls
    back to the products page.
    """
    # Retrieve the product or return 404 if it doesn't exist
    product = get_object_or_404(Product, id=product_id)

    # Get quantity from POST data, defaulting to 1 if not provided
    quantity = int(request.POST.get('quantity', 1))

    # Get the selected size if the product has sizes
    size = request.POST.get('product_size')

    # Get the user's cart or create one if it doesn't exist
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Get or create a cart item for this product and size combination
    # defaults ensures price is only set when the item is first created
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        size=size,
        defaults={'price': product.price, 'quantity': quantity}
    )

    if not created:
        # Item already exists in cart — increment quantity
        cart_item.quantity += quantity
        cart_item.save()

    # Show success toast message to confirm item was added
    messages.success(request, f"{product.name} has been added to your cart!")

    # Redirect to the URL specified in the form or fall back to products
    redirect_url = request.POST.get('redirect_url')

    return redirect(redirect_url or 'products:products')


@login_required
def adjust_cart(request, item_id):
    """
    Update the quantity of a specific cart item.
    Retrieves the cart item by ID and updates its quantity
    to the value submitted in the POST request.
    If the quantity is set to 0 the item is removed from the cart.
    Redirects back to the cart page after updating.
    """
    # Retrieve the cart item ensuring it belongs to the current user
    cart_item = get_object_or_404(
        CartItem, id=item_id, cart__user=request.user
    )

    # Get the new quantity from the POST request
    quantity = int(request.POST.get('quantity', 0))

    if quantity > 0:
        # Update the cart item with the new quantity
        cart_item.quantity = quantity
        cart_item.save()
    else:
        # Remove the item if quantity is set to 0
        cart_item.delete()

    return redirect('cart:view_cart')


@login_required
def remove_from_cart(request, item_id):
    """
    Remove a cart item completely from the user's cart.
    Finds the cart item by ID, verifies it belongs to the
    current user, deletes it and redirects back to the cart
    with a success message.
    """
    # Find the cart item ensuring it belongs to the current user
    cart_item = get_object_or_404(
        CartItem, id=item_id, cart__user=request.user
    )

    # Delete the cart item permanently
    cart_item.delete()

    # Show success message to confirm removal
    messages.success(request, "Item removed from your cart!")

    return redirect('cart:view_cart')