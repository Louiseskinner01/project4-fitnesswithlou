from django.shortcuts import render
from .models import Product

# Create your views here.
def all_products(request):
    # Retrieves all products from the database
    products = Product.objects.all()

    # Sends the products to the template      
    context = {
        'products': products,
    }

    # Loads the HTML template
    return render(request, 'products/products.html', context)