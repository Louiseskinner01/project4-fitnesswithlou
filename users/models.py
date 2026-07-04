from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class UserProfile(models.Model):
    """
    Stores additional information for a registered user.
    Extends Django's built in User model using a OneToOneField
    to add delivery information and Stripe account details.
    The profile is automatically created or retrieved using
    get_or_create in the profile view.
    Default delivery fields are pre-filled in the checkout form
    to speed up the purchase process for returning customers.
    Stripe fields link the user's Django account to their
    Stripe customer and subscription records.
    """

    # Predefined fitness experience level choices
    # Available for future use in personalising the user experience
    EXPERIENCE_LEVEL = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    # Predefined fitness goal choices
    # Available for future use in personalising the user experience
    FITNESS_GOALS = [
        ('weight_loss', 'Weight Loss'),
        ('muscle_gain', 'Muscle Gain'),
        ('general_fitness', 'General Fitness'),
    ]

    # One to one link to Django's built in User model
    # CASCADE deletes the profile if the user account is deleted
    # OneToOneField ensures each user can only have one profile
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Default delivery information saved from previous orders
    # All fields are optional (null and blank) as users may not
    # have completed a purchase yet
    default_phone_number = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    default_street_address1 = models.CharField(
        max_width=80,
        null=True,
        blank=True
    )

    default_street_address2 = models.CharField(
        max_length=80,
        null=True,
        blank=True
    )

    default_town_or_city = models.CharField(
        max_length=40,
        null=True,
        blank=True
    )

    default_postcode = models.CharField(
        max_length=40,
        null=True,
        blank=True
    )

    # CountryField provides a dropdown of all countries
    # blank_label sets the default empty option text
    default_country = CountryField(
        blank_label='Country*',
        null=True,
        blank=True
    )

    # Stripe customer ID — links this user to their Stripe customer record
    # Set when the user first subscribes to a membership plan
    # Used to retrieve and manage their Stripe account
    stripe_customer_id = models.CharField(
        max_length=254,
        null=True,
        blank=True
    )

    # Stripe subscription ID — links this user to their active subscription
    # Set when a subscription is activated via the webhook handler
    # Cleared when the subscription is cancelled
    stripe_subscription_id = models.CharField(
        max_length=254,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.username
