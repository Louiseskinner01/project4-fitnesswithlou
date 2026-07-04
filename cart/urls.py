from django.urls import path
from . import views

# Cart app namespace — used to reference URLs as 'cart:url_name'
app_name = 'cart'

urlpatterns = [
    # Display the user's shopping cart
    path('', views.view_cart, name='view_cart'),

    # Add a product to the cart
    # product_id identifies which product to add
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    # Update the quantity of a specific cart item
    # item_id identifies which CartItem to adjust
    path(
        'adjust_cart/<int:item_id>/',
        views.adjust_cart,
        name='adjust_cart'
    ),

    # Remove a specific item from the cart completely
    # item_id identifies which CartItem to delete
    path(
        'remove/<int:item_id>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),
]