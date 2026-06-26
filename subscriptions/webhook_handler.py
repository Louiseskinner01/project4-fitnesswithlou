import stripe
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import UserSubscription, SubscriptionPlan
from users.models import UserProfile


def send_subscription_confirmation(user, subscription):
    """Send confirmation email after subscription activated"""
    subject = render_to_string(
        'subscriptions/confirmation_emails/confirmation_subject.txt',
        {'subscription': subscription}
    ).strip()

    body = render_to_string(
        'subscriptions/confirmation_emails/confirmation_body.txt',
        {
            'user': user,
            'subscription': subscription,
            'contact_email': settings.DEFAULT_FROM_EMAIL
        }
    )

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [user.email]
    )


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

        stripe.api_key = settings.STRIPE_SECRET_KEY
        subscription = stripe.Subscription.retrieve(subscription_id)
        price_id = subscription['items']['data'][0]['price']['id']

        price_plan_map = {
            settings.STRIPE_PRICE_BASIC: 'basic',
            settings.STRIPE_PRICE_PREMIUM: 'premium',
            settings.STRIPE_PRICE_VIP: 'vip',
        }
        plan_name = price_plan_map.get(price_id)

        if plan_name:
            plan = SubscriptionPlan.objects.get(name=plan_name)

            UserSubscription.objects.filter(
                user=profile.user,
                status='active'
            ).update(status='cancelled')

            user_subscription = UserSubscription.objects.create(
                user=profile.user,
                plan=plan,
                status='active'
            )

            # ✅ Send confirmation email
            send_subscription_confirmation(profile.user, user_subscription)
            print(
                f"Subscription activated and"
                f"email sent for {profile.user.username}")

    except UserProfile.DoesNotExist:
        print(f"No profile found for customer {customer_id}")


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
        print(f"Subscription cancelled for {profile.user.username}")

    except UserProfile.DoesNotExist:
        print(f"No profile found for customer {customer_id}")
