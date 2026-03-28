from django.shortcuts import render, get_object_or_404
from .models import Product


def all_products(request):
    """ A view to show all products """
    # Retrieves all products from the database
    products = Product.objects.all()

    # Sends the products to the template      
    context = {
        'products': products,
    }

    # Loads the HTML template
    return render(request, 'products/products.html', context)

def product_details(request, product_id):
    """ A view to show individual proect details """
    
    product = get_object_or_404(Product, pk=product_id)
    # Sends the products to the template      
    context = {
        'product': product,
    }

    # Loads the HTML template
    return render(request, 'products/product_details.html', context)