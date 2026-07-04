from django.db import models
from django.contrib.auth.models import User


class SubscriptionPlan(models.Model):
    """
    Stores the details of an available membership plan.
    Each plan has a name, price, billing cycle and description.
    Plans are created and managed through the Django admin panel
    and linked to Stripe price IDs in settings.py.
    """

    # Predefined choices for the subscription tier
    # Restricts the name field to only these three valid options
    PLAN_CHOICES = [
        ('basic', 'Basic Membership'),
        ('premium', 'Premium Membership'),
        ('vip', 'VIP Membership'),
    ]

    # This stores the selected plan from the choices above
    name = models.CharField(max_length=50, choices=PLAN_CHOICES)

    # This gives the price of the subscription plan
    price = models.DecimalField(max_digits=6, decimal_places=2)

    # Defines how often the user is billed
    # Defaults to monthly as this is the most common billing cycle
    billing_cycle = models.CharField(
        max_length=20,
        choices=[
            ('monthly', 'Monthly'),
            ('yearly', 'Yearly'),
        ],
        default='monthly'
    )

    # This provides a description of the plan and what it includes
    # Displayed on the subscription plans page
    description = models.TextField()

    def __str__(self):
        return self.get_name_display()


# This model connects the user to the subscription plan
class UserSubscription(models.Model):
    """
    Stores an individual user's subscription to a plan.
    Links a user to a SubscriptionPlan and tracks the
    subscription status, start date, end date and whether
    it is set to cancel at the end of the billing period.
    A user should only have one active subscription at a time.
    """

    # Link to the Django user who holds this subscription
    # CASCADE deletes the subscription if the user account is deleted
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # This links to the chosen subscription plan
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)

    # This stores the date when the subscription starts
    start_date = models.DateTimeField(auto_now_add=True)

    # Status of the subscription (active, cancelled, or expired)
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ]

    # Current status of the subscription
    # Defaults to active when a new subscription is created
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active')

    # When True, the subscription will not renew at the end of the
    # current billing period — the user retains access until period end
    # This is set via Stripe's cancel_at_period_end feature
    cancel_at_period_end = models.BooleanField(default=False)
    
    # This stores the date when the subscription ends or is due to expire
    # Null and blank as this is only set when a subscription is cancelled
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"
