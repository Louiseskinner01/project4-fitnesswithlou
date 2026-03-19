from django.db import models
from django.contrib.auth.models import User


class SubscriptionPlan(models.Model):

    # Predefined choices allowing the user to select a specific subscription plan
    PLAN_CHOICES = [
        ('basic', 'Basic Membership'),
        ('premium', 'Premium Membership'),
        ('vip', 'VIP Membership'),
    ]

    # This stores the selected plan from the choices above
    name = models.CharField(max_length=50, choices=PLAN_CHOICES)
    
    # This gives the price of the subscription plan
    price = models.DecimalField(max_digits=6, decimal_places=2) 

    # The below fields are from ChatGPT to help imporve the users experience and make the app more sophisticated.
    #Defines how often the user is billed (monthly or annually)
    billing_cycle = models.CharField(
        max_length=20, 
        choices= [
            ('monthly', 'Monthly'),
            ('yearly', 'Yearly'),
        ], 
        default='monthly'
    )

    # This provides a description of the plan and what it includes
    description = models.TextField()

    def __str__(self):
        return self.get_name_display()

# This model connects the user to the subscription plan
class UserSubscription(models.Model):

    # This links a subscription to a specific user
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # This links to the chosen subscription plan
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)

    # This stores the date when the subscription starts
    start_date = models.DateTimeField(auto_now_add=True)

    # This stores the date when the subscription ends
    end_date = models.DateTimeField(null=True, blank=True)

    # Status of the subscription (active, cancelled, or expired)
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"