from django.urls import path
from . import views

# Products app namespace — used to reference URLs as 'products:url_name'
app_name = 'products'

urlpatterns = [
    # Display all products with optional category filter and search
    path('', views.all_products, name='products'),

    # Add a new product — superusers only
    path('add/', views.add_product, name='add_product'),

    # Edit an existing product — superusers only
    # product_id identifies which product to edit
    path(
        'edit/<int:product_id>/',
        views.edit_product,
        name='edit_product'
    ),

    # Delete an existing product — superusers only
    # product_id identifies which product to delete
    path(
        'delete/<int:product_id>/',
        views.delete_product,
        name='delete_product'
    ),

    # Display the detail page for a single product
    # product_id identifies which product to display
    path(
        '<int:product_id>/',
        views.product_details,
        name='product_details'
    ),
]