import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SubscriptionPlan, UserSubscription

stripe.api_key = settings.STRIPE_SECRET_KEY

PRICE_MAP = {
    'basic': settings.STRIPE_PRICE_BASIC,
    'premium': settings.STRIPE_PRICE_PREMIUM,
    'vip': settings.STRIPE_PRICE_VIP,
}

def subscription_plans(request):
    plans = SubscriptionPlan.objects.all()
    context = {
        'plans': plans
    }
    return render(request, 'subscriptions/plans.html', context)


@login_required
def subscribe(request, plan_id):
    plan = get_object_or_404(SubscriptionPlan, id=plan_id)
    price_id = PRICE_MAP.get(plan.name)

    if not price_id:
        messages.error(request, 'Invalid plan selected.')
        return redirect('subscriptions:subscription_plans')

       # Check for existing active subscription
    existing_subscription = UserSubscription.objects.filter(
        user=request.user,
        status='active'
    ).first()

    if existing_subscription:
        messages.error(request, f'You already have an active {existing_subscription.plan.get_name_display()} subscription. Please cancel it before subscribing to a new plan.')
        return redirect('subscriptions:subscription_plans')

    profile = request.user.userprofile

    # Create or retrieve Stripe customer
    if not profile.stripe_customer_id:
        customer = stripe.Customer.create(
            email=request.user.email,
            name=request.user.get_full_name() or request.user.username,
        )
        profile.stripe_customer_id = customer.id
        profile.save()

    # Create Stripe checkout session for subscription
    session = stripe.checkout.Session.create(
        customer=profile.stripe_customer_id,
        payment_method_types=['card'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='subscription',
        success_url=request.build_absolute_uri('/subscriptions/success/'),
        cancel_url=request.build_absolute_uri('/subscriptions/'),
    )

    return redirect(session.url, code=303)


@login_required
def subscription_success(request):
    messages.success(request, 'You have successfully subscribed!')
    return render(request, 'subscriptions/success.html')


@login_required  
def subscription_cancel(request):
    return render(request, 'subscriptions/cancel.html')