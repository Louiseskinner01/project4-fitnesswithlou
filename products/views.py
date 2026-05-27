from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category
from .forms import ProductForm


def all_products(request):
    """ A view to show all products """
    # Retrieves all products from the database
    products = Product.objects.all()
    query = None
    categories = None

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

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
    
    sizes = []

    if product.sizes:
        sizes = product.sizes.split(',')

    
    # Sends the products to the template      
    context = {
        'product': product,
        'sizes': sizes,
    }

    # Loads the HTML template
    return render(request, 'products/product_details.html', context)


def add_product(request): 
    """ Add a product to the online store """ 
    form = ProductForm()
    template = 'products/add_products.html' 
    context = {
        'form': form,
    }

    return render(request, template, context)

def edit_product(request, product_id): 
    """ Edit a product """ 
    
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.info(request, f'Product {product.name}: {product_id} successfully updated! ')
            return redirect('products:product_details', product.id)
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.success(request, f'Product {product.name}: {product_id} successfully updated! ')


    template = 'products/edit_products.html' 
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


def delete_product(request, product_id): 
    """ Delete a product """ 

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product successfully deleted!')

    return(redirect(reverse('products:products')))