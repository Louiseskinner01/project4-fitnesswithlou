from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from .models import Product, Category
from .forms import ProductForm


def all_products(request):
    """
    Display all products with optional filtering and search.
    Supports filtering by category via GET parameters and
    full text search across product name and description
    using Django's Q objects for complex queries.
    Accessible to all users including unauthenticated visitors.
    """
    # Retrieve all products from the database
    products = Product.objects.all()
    query = None
    categories = None

    if request.GET:
        # Filter products by category if category parameter is present
        if 'category' in request.GET:
            # Split comma separated category names into a list
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            # Get the Category objects for display in the template
            categories = Category.objects.filter(name__in=categories)

        # Filter products by search query if q parameter is present
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                # Redirect with error if search field was submitted empty
                messages.error(
                    request,
                    "You didn't enter any search criteria!"
                )
                return redirect(reverse('products:products'))

            # Search across both name and description fields
            # Q objects allow OR queries — matches either field
            queries = (
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )
            products = products.filter(queries)

    # Pass filtered products and search term to the template
    context = {
        'products': products,
        'search_term': query,
    }

    return render(request, 'products/products.html', context)


def product_details(request, product_id):
    """
    Display the detail page for a single product.
    Retrieves the product by its primary key and splits
    the sizes string into a list for display in the template.
    Accessible to all users including unauthenticated visitors.
    """
    # Retrieve the product or return 404 if it doesn't exist
    product = get_object_or_404(Product, pk=product_id)
    sizes = []

    # Split the comma separated sizes string into a list
    # e.g. 'xs,s,m,l,xl' becomes ['xs', 's', 'm', 'l', 'xl']
    if product.sizes:
        sizes = product.sizes.split(',')

    context = {
        'product': product,
        'sizes': sizes,
    }

    return render(request, 'products/product_details.html', context)


@login_required
def add_product(request):
    """
    Allow superusers to add a new product to the store.
    GET request: renders the empty product form.
    POST request: validates and saves the new product,
    then redirects to the product detail page.
    Raises PermissionDenied (403) if a non-superuser attempts access.
    Requires the user to be logged in.
    """
    # Restrict access to superusers only
    # Raises 403 Forbidden for regular authenticated users
    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method == 'POST':
        # Bind the form with POST data and any uploaded files
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product added successfully!')
            # Redirect to the new product's detail page
            return redirect('products:product_details', product.id)
        else:
            messages.error(
                request,
                'Failed to add product. Please check the form.'
            )
    else:
        # GET request — render empty product form
        form = ProductForm()

    template = 'products/add_products.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """
    Allow superusers to edit an existing product.
    GET request: renders the product form pre-filled with
    the existing product data.
    POST request: validates and saves the updated product,
    then redirects to the product detail page.
    Raises PermissionDenied (403) if a non-superuser attempts access.
    Requires the user to be logged in.
    """
    # Restrict access to superusers only
    if not request.user.is_superuser:
        raise PermissionDenied

    # Retrieve the product to edit or return 404 if not found
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        # Bind the form with POST data, uploaded files and existing instance
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.info(
                request,
                f'Product {product.name}: {product_id} successfully updated!'
            )
            # Redirect to the updated product's detail page
            return redirect('products:product_details', product.id)
        else:
            messages.error(
                request,
                'Failed to update product. Please ensure the form is valid.'
            )
    else:
        # GET request — pre-fill the form with existing product data
        form = ProductForm(instance=product)
        messages.success(
            request,
            f'Product {product.name}: {product_id} successfully updated!'
        )

    template = 'products/edit_products.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """
    Allow superusers to delete a product from the store.
    Retrieves the product by ID, deletes it from the database
    and redirects to the products page with a success message.
    A confirmation prompt is handled in the template via JavaScript
    before this view is called.
    Raises PermissionDenied (403) if a non-superuser attempts access.
    Requires the user to be logged in.
    """
    # Restrict access to superusers only
    if not request.user.is_superuser:
        raise PermissionDenied

    # Retrieve the product or return 404 if it doesn't exist
    product = get_object_or_404(Product, pk=product_id)

    # Delete the product from the database
    product.delete()
    messages.success(request, 'Product successfully deleted!')

    return redirect(reverse('products:products'))
    