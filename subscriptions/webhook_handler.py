import stripe
from django.conf import settings
from django.http import HttpResponse
from .models import UserSubscription, SubscriptionPlan
from users.models import UserProfile


def handle_subscription_webhook(event):
    """Handle Stripe subscription webhook events"""
    
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_checkout_completed(session)

    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        handle_subscription_cancelled(subscription)

    return HttpResponse(status=200)


def handle_checkout_completed(session):
    """Activate subscription after successful checkout"""
    customer_id = session.customer
    subscription_id = session.subscription

    if not customer_id or not subscription_id:
        return

    try:
        profile = UserProfile.objects.get(stripe_customer_id=customer_id)
        profile.stripe_subscription_id = subscription_id
        profile.save()

        # Get the price ID from the subscription
        stripe.api_key = settings.STRIPE_SECRET_KEY
        subscription = stripe.Subscription.retrieve(subscription_id)
        price_id = subscription['items']['data'][0]['price']['id']

        # Map price ID to plan
        price_plan_map = {
            settings.STRIPE_PRICE_BASIC: 'basic',
            settings.STRIPE_PRICE_PREMIUM: 'premium',
            settings.STRIPE_PRICE_VIP: 'vip',
        }
        plan_name = price_plan_map.get(price_id)

        if plan_name:
            plan = SubscriptionPlan.objects.get(name=plan_name)
            # Cancel any existing subscriptions
            UserSubscription.objects.filter(
                user=profile.user,
                status='active'
            ).update(status='cancelled')

            # Create new active subscription
            UserSubscription.objects.create(
                user=profile.user,
                plan=plan,
                status='active'
            )
            print(f" Subscription activated for {profile.user.username}")

    except UserProfile.DoesNotExist:
        print(f" No profile found for customer {customer_id}")


def handle_subscription_cancelled(subscription):
    """Cancel subscription when deleted in Stripe"""
    customer_id = subscription.customer

    try:
        profile = UserProfile.objects.get(stripe_customer_id=customer_id)
        UserSubscription.objects.filter(
            user=profile.user,
            status='active'
        ).update(status='cancelled')
        profile.stripe_subscription_id = None
        profile.save()
        print(f" Subscription cancelled for {profile.user.username}")

    except UserProfile.DoesNotExist:
        print(f" No profile found for customer {customer_id}")