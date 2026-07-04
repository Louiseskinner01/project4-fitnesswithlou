import stripe
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import UserSubscription, SubscriptionPlan
from users.models import UserProfile


def send_subscription_confirmation(user, subscription):
    """
    Send a subscription confirmation email to the user
    after their membership has been successfully activated.
    Renders both subject and body from email templates
    and sends via Django's send_mail function.
    """
    # Render email subject from template and strip whitespace
    subject = render_to_string(
        'subscriptions/confirmation_emails/confirmation_subject.txt',
        {'subscription': subscription}
    ).strip()

    # Render email body from template with user and subscription context
    body = render_to_string(
        'subscriptions/confirmation_emails/confirmation_body.txt',
        {
            'user': user,
            'subscription': subscription,
            'contact_email': settings.DEFAULT_FROM_EMAIL
        }
    )

    # Send the confirmation email to the user
    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [user.email]
    )


def handle_subscription_webhook(event):
    """
    Route incoming Stripe webhook events to the appropriate handler.
    Currently handles two event types:
    - checkout.session.completed: fires when a subscription checkout succeeds
    - customer.subscription.deleted: fires when a subscription is cancelled
    Returns a 200 response to acknowledge receipt of the webhook.
    """
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_checkout_completed(session)

    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        handle_subscription_cancelled(subscription)

    return HttpResponse(status=200)


def handle_checkout_completed(session):
    """
    Activate a user's subscription after a successful Stripe checkout.
    Retrieves the Stripe customer and subscription IDs from the session,
    maps the Stripe price ID to the corresponding plan in the database,
    cancels any existing active subscriptions to prevent duplicates,
    creates a new active UserSubscription record, and sends a
    confirmation email to the user.
    """
    # Extract the Stripe customer and subscription IDs from the session
    customer_id = session.customer
    subscription_id = session.subscription

    # Exit early if either ID is missing — cannot process without both
    if not customer_id or not subscription_id:
        return

    try:
        # Find the user profile associated with this Stripe customer
        profile = UserProfile.objects.get(stripe_customer_id=customer_id)
        
        # Save the subscription ID to the user's profile for future reference
        profile.stripe_subscription_id = subscription_id
        profile.save()

        # Retrieve the full subscription object from Stripe
        # to get the price ID of the plan they subscribed to
        stripe.api_key = settings.STRIPE_SECRET_KEY
        subscription = stripe.Subscription.retrieve(subscription_id)
        price_id = subscription['items']['data'][0]['price']['id']

        # Map Stripe price IDs to internal plan names
        # Price IDs are configured in Django settings
        price_plan_map = {
            settings.STRIPE_PRICE_BASIC: 'basic',
            settings.STRIPE_PRICE_PREMIUM: 'premium',
            settings.STRIPE_PRICE_VIP: 'vip',
        }
        plan_name = price_plan_map.get(price_id)

        if plan_name:
            plan = SubscriptionPlan.objects.get(name=plan_name)

            # Cancel any existing active subscriptions before creating
            # a new one to prevent a user having multiple active plans
            UserSubscription.objects.filter(
                user=profile.user,
                status='active'
            ).update(status='cancelled')

            # Create the new active subscription record
            user_subscription = UserSubscription.objects.create(
                user=profile.user,
                plan=plan,
                status='active'
            )

            # Send confirmation email to notify the user
            send_subscription_confirmation(profile.user, user_subscription)
            print(
                f"Subscription activated and"
                f"email sent for {profile.user.username}")

    except UserProfile.DoesNotExist:
        print(f"No profile found for customer {customer_id}")


def handle_subscription_cancelled(subscription):
    """
    Handle cancellation of a subscription in Stripe.
    Finds the associated user profile using the Stripe customer ID,
    updates all active UserSubscription records to cancelled status,
    and clears the subscription ID from the user's profile.
    """
    # Extract the Stripe customer ID from the subscription object
    customer_id = subscription.customer

    try:
        # Find the user profile associated with this Stripe customer
        profile = UserProfile.objects.get(stripe_customer_id=customer_id)
        
        # Update all active subscriptions for this user to cancelled
        UserSubscription.objects.filter(
            user=profile.user,
            status='active'
        ).update(status='cancelled')

        # Clear the subscription ID from the profile
        # as it is no longer active
        profile.stripe_subscription_id = None
        profile.save()
        print(f"Subscription cancelled for {profile.user.username}")

    except UserProfile.DoesNotExist:
        # Log if no profile is found for this Stripe customer
        print(f"No profile found for customer {customer_id}")
