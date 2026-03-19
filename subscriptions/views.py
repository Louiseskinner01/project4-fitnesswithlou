from django.shortcuts import render, redirect
from.models import UserSubscription, SubscriptionPlan
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages


def subscription_plans(request):
    plans = SubscriptionPlan.objects.all()

    # Context dicstionary
    context = {
        'plans': plans
    }

    return render(request, 'subscriptions/plans.html', context)

@login_required
def subscribe(request, plan_id):

    plan = get_object_or_404(SubscriptionPlan, id=plan_id)

    # Prevents duplicate subscriptions
    UserSubscription.objects.obejct.get_or_create(
        user=request.user,
        plan=plan
    )

    # Message confirming that the user has subscribed to a specific plan
    messages.success(request, f" You have subscribes to {plan.name}!")
    
    # Return the user to the subscription plans template
    return redirect('subscriptions:subscribe')