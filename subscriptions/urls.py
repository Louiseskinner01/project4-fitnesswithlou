from django.urls import path
from . import views

# Subscriptions app namespace — used to reference URLs as 'subscriptions:url_name'
app_name = 'subscriptions'

urlpatterns = [
    # Display all available subscription plans (Basic, Premium, VIP)
    path('', views.subscription_plans, name='subscription_plans'),

    # Initiate a Stripe checkout session for a specific plan
    # plan_id identifies which SubscriptionPlan the user wants to subscribe to
    path(
        'subscribe/<int:plan_id>/',
        views.subscribe,
        name='subscribe'
    ),

    # Success page — displayed after a successful subscription payment
    path('success/', views.subscription_success, name='subscription_success'),

    # Cancel an active subscription — sets cancel_at_period_end in Stripe
    # so the user retains access until the end of their billing period
    path('cancel/', views.cancel_subscription, name='cancel_subscription'),

    # Confirmation page shown after a subscription has been cancelled
    path(
        'cancelled/',
        views.subscription_cancelled,
        name='subscription_cancelled'
    ),
]