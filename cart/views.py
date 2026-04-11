from django.shortcuts import render, redirect, reverse, get_object_or_404 
from django.http import HttpResponse
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from products.models import Product
from django.contrib import messages

# Ensures only authenticated users can access the cart and its functionality
@login_required

# Enables logged in users to view their shopping cart
def view_cart(request):

# Get the users cart or create one if the cart doesn't exist
    cart, created = Cart.objects.get_or_create(user=request.user)

# Context dictionary: Sends data (cart object and cart items) from the view to the template
    context = {
        'cart' : cart,
        'items' : cart.items.all()
    }

# Render the cart template and display contents for the cart
    return render(request, 'cart/shopping_cart.html', context)


# This is a sample code from chatGPT to enable the use to add and remove items from their cart
@login_required
def add_to_cart(request, product_id):
    """ Add a product and increase the quantity which will be reflected in the shopping bag """

    # Get object (product) from database, if object doesn't exist then display 404 error page
    product = get_object_or_404(Product, id=product_id)

    quantity = int(request.POST.get('quantity', 1))
    size = request.POST.get('product_size')  # Gets size if exists
    
    # Get cart, or create a cart if it doesn't exist
    cart, created = Cart.objects.get_or_create(user=request.user)
 
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        size=size,
        # Ensures the price is only set once the time is add
        defaults={'price': product.price, 'quantity': quantity}
    )

    if not created:
        # If the item already exists in the cart then increase the quantity to what the user has specified
        cart_item.quantity += quantity
        cart_item.save()
       

    # Confirmation that item has been added to the cart
    messages.success(request, f"{product.name} has been added to your cart!")

    redirect_url = request.POST.get('redirect_url')

    return redirect(redirect_url or 'products:products')


@login_required
def adjust_cart(request, item_id):
    """ Adjust the quantity of a cart item (database-based, replaces session code) """

    # Get the cart item from the database
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    # Get the new quantity from the POST request
    quantity = int(request.POST.get('quantity', 0))

    if quantity > 0:
        # Update the quantity
        cart_item.quantity = quantity
        cart_item.save()
        
    else:
        # Delete the cart item if quantity is 0
        cart_item.delete()

    # messages.success(request, f" Updated {'product':product.name} to your cart!")
    return redirect('cart:view_cart')
    


@login_required
def remove_from_cart(request, item_id):
    """
    Remove a cart item completely, regardless of quantity or size.
    """
    # Find the item in the current user's cart
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    # Delete it
    cart_item.delete()

    # Optional: give user feedback
    messages.success(request, "Item removed from your cart!")

    # Redirect back to the cart page
    return redirect('cart:view_cart')