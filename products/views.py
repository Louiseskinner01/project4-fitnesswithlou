from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product


def all_products(request):
    """ A view to show all products """
    # Retrieves all products from the database
    products = Product.objects.all()
    query = None

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products:products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    # Sends the products to the template      
    context = {
        'products': products,
        'search_term': query,
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