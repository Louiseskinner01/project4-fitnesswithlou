from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


# Create your models here.
class UserProfile(models.Model):

    EXPERIENCE_LEVEL = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    FITNESS_GOALS = [
        ('weight_loss', 'Weight Loss'),
        ('muscle_gain', 'Muscle Gain'),
        ('general_fitness', 'General Fitness'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    default_phone_number = models.CharField(
        max_length=20,
        null=True,
        blank=True)

    default_street_address1 = models.CharField(
        max_length=80,
        null=True,
        blank=True)

    default_street_address2 = models.CharField(
        max_length=80,
        null=True,
        blank=True)

    default_town_or_city = models.CharField(
        max_length=40,
        null=True,
        blank=True)

    default_postcode = models.CharField(max_length=40, null=True, blank=True)

    default_country = CountryField(
        blank_label='Country*',
        null=True,
        blank=True)

    stripe_customer_id = models.CharField(
        max_length=254,
        null=True,
        blank=True)

    stripe_subscription_id = models.CharField(
        max_length=254,
        null=True,
        blank=True)

    def __str__(self):
        return self.user.username
