from django.urls import path
from . import views
from .webhooks import webhook

# Checkout app namespace — used to reference URLs as 'checkout:url_name'
app_name = 'checkout'

urlpatterns = [
    # Main checkout page — displays order form and Stripe payment element
    path('', views.checkout, name='checkout'),
    
    # Success page — displayed after a successful payment
    # order_number is passed to identify and display the completed order
    path('checkout_success/<order_number>/',
         views.checkout_success,
         name='checkout_success'),
    
    # Stripe webhook endpoint — receives payment event notifications from Stripe
    # This URL must match the endpoint configured in the Stripe dashboard
    path('wh/', webhook, name='stripe_webhook'),
]
