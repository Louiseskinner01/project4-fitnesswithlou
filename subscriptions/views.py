import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SubscriptionPlan, UserSubscription

# Set the Stripe API key from Django settings
# This is used for all Stripe API calls throughout this file
stripe.api_key = settings.STRIPE_SECRET_KEY

# Maps internal plan names to their corresponding Stripe price IDs
# Price IDs are configured in settings.py and created in the Stripe dashboard
PRICE_MAP = {
    'basic': settings.STRIPE_PRICE_BASIC,
    'premium': settings.STRIPE_PRICE_PREMIUM,
    'vip': settings.STRIPE_PRICE_VIP,
}


def subscription_plans(request):
    """
    Display all available subscription plans.
    Retrieves all SubscriptionPlan objects from the database
    and renders them on the plans page for the user to choose from.
    Accessible to both authenticated and unauthenticated users.
    """
    plans = SubscriptionPlan.objects.all()
    context = {
        'plans': plans
    }
    return render(request, 'subscriptions/plans.html', context)


@login_required
def subscribe(request, plan_id):
    """
    Initiate a Stripe checkout session for a subscription plan.
    Validates the selected plan, checks for existing active
    subscriptions to prevent duplicates, creates or retrieves
    a Stripe customer for the user, then redirects to a Stripe
    hosted checkout page to complete the subscription payment.
    Requires the user to be logged in.
    """
    # Retrieve the selected plan or return 404 if not found
    plan = get_object_or_404(SubscriptionPlan, id=plan_id)

    # Get the corresponding Stripe price ID for this plan
    price_id = PRICE_MAP.get(plan.name)

    # Redirect if the plan name doesn't match any Stripe price ID
    if not price_id:
        messages.error(request, 'Invalid plan selected.')
        return redirect('subscriptions:subscription_plans')

    # Check if the user already has an active subscription
    # to prevent them from subscribing to multiple plans simultaneously
    existing_subscription = UserSubscription.objects.filter(
        user=request.user,
        status='active'
    ).first()

    if existing_subscription:
        messages.error(
            request,
            (
                f'You already have an active '
                f'{existing_subscription.plan.get_name_display()}'
                f' subscription. Please cancel it '
                f'before subscribing to a new plan.'
            )
        )
        return redirect('subscriptions:subscription_plans')

    # Get the user's profile to access Stripe customer information
    profile = request.user.userprofile

    # Create a new Stripe customer if one doesn't exist for this user
    # This links the user's Django account to their Stripe account
    if not profile.stripe_customer_id:
        customer = stripe.Customer.create(
            email=request.user.email,
            name=request.user.get_full_name() or request.user.username,
        )
        profile.stripe_customer_id = customer.id
        profile.save()

    # Create a Stripe checkout session for the subscription
    # The session handles the payment UI and processes the subscription
    session = stripe.checkout.Session.create(
        customer=profile.stripe_customer_id,
        payment_method_types=['card'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='subscription',
        # Redirect URLs after successful or cancelled payment
        success_url=request.build_absolute_uri('/subscriptions/success/'),
        cancel_url=request.build_absolute_uri('/subscriptions/'),
    )

    # Redirect to the Stripe hosted checkout page
    # HTTP 303 ensures the redirect uses a GET request
    return redirect(session.url, code=303)


@login_required
def subscription_success(request):
    """
    Display a success message after a subscription is activated.
    This page is shown after the user completes the Stripe
    checkout session. The actual subscription activation is
    handled by the webhook handler, not this view.
    Requires the user to be logged in.
    """
    messages.success(request, 'You have successfully subscribed!')
    return render(request, 'subscriptions/success.html')


@login_required
def cancel_subscription(request):
    """
    Cancel the user's active subscription via Stripe.
    Uses Stripe's cancel_at_period_end feature so the user
    retains access until the end of their current billing period
    rather than being cut off immediately.
    Updates the local UserSubscription status to cancelled
    and redirects to the cancellation confirmation page.
    Requires the user to be logged in.
    """
    profile = request.user.userprofile

    # Check if the user has an active Stripe subscription to cancel
    if not profile.stripe_subscription_id:
        messages.error(request, 'No active subscription found.')
        return redirect('users:profile')

    try:
        # Cancel at period end rather than immediately
        # This means the user keeps access until their billing period expires
        stripe.Subscription.modify(
            profile.stripe_subscription_id,
            cancel_at_period_end=True
        )

        # Update the local subscription status to reflect the cancellation
        # This ensures the profile page shows the correct status immediately
        UserSubscription.objects.filter(
            user=request.user,
            status='active'
        ).update(status='cancelled')

        messages.success(
            request,
            'Your subscription has been cancelled. '
            'You will have access until the '
            'end of your current billing period.'
        )

    except stripe.error.StripeError as e:
        # Handle any Stripe API errors gracefully
        messages.error(request, f'Error cancelling subscription: {e}')

    return redirect('subscriptions:subscription_cancelled')


@login_required
def subscription_cancelled(request):
    """
    Display the subscription cancellation confirmation page.
    Shown after a user successfully cancels their subscription.
    Requires the user to be logged in.
    """
    return render(request, 'subscriptions/cancel.html')