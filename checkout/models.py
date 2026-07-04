import uuid

from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.conf import settings

from django_countries.fields import CountryField

from products.models import Product


class Order(models.Model):
    """
    Stores a single customer order.
    Contains all delivery information, payment details and
    order totals. Each order is linked to a user and can
    contain multiple line items (OrderLineItem).
    """

    # Link to the Django user who placed the order
    # SET_NULL allows orders to persist if a user account is deleted
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True,
        blank=True, related_name='orders'
    )

    # Unique order reference generated automatically via UUID
    order_number = models.CharField(max_length=32, null=False, editable=False)
    
    # Customer contact and delivery information
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    
    # CountryField provides a dropdown of all countries
    country = CountryField(
        blank_label='Country *',
        null=False,
        blank=False)

    # Order date set automatically when the order is created
    date = models.DateTimeField(auto_now_add=True)
    
    # Financial fields — calculated automatically via update_total()
    delivery_cost = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=False,
        default=0)
    order_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        default=0)
    grand_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        default=0)
    
    # Link to user profile for saving delivery information
    # SET_NULL allows orders to persist if a profile is deleted
    user_profile = models.ForeignKey(
        'users.UserProfile',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='orders'
    )

    # Stores the original bag contents as JSON for webhook reference
    # Used to recreate the order if the webhook fires before the view saves it
    original_bag = models.TextField(null=False, blank=False, default='')
    
    # Stripe PaymentIntent ID — used to match webhook events to orders
    # and prevents duplicate order creation
    stripe_pid = models.CharField(
        max_length=254,
        null=False,
        blank=False,
        default='')

    def _generate_order_number(self):
        """
        Generate a random unique order number using UUID.
        Takes the first 8 characters of a UUID hex string
        and converts to uppercase for readability.
        e.g. 'A1B2C3D4'
        """
        return uuid.uuid4().hex[:8].upper()

    def update_total(self):
        """
        Recalculate and save the order grand total.
        Called every time a line item is added or updated.
        Sums all line item totals, applies delivery charge
        if the order total is below the free delivery threshold,
        then saves the updated totals to the database.
        """
        # Sum all line item totals — default to 0 if no items exist
        self.order_total = self.lineitems.aggregate(
             Sum('lineitem_total'))['lineitem_total__sum'] or 0
        
        # Apply delivery charge if below free delivery threshold
        if self.order_total < settings.FREE_DELIVERY_ABOVE:
            self.delivery_cost = self.order_total * settings.DELIVERY_PERCENTAGE / 100
        else:
            # Free delivery threshold met — no delivery charge
            self.delivery_cost = 0
        
        # Calculate the final grand total
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the default save method to automatically generate
        an order number if one hasn't been assigned yet.
        Ensures every order has a unique reference number.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    """
    Stores a single product within an order.
    Each line item represents one product with a specific
    quantity and optional size. Multiple line items can
    belong to the same order.
    """
    # Link to the parent order — CASCADE deletes line items if order is deleted
    order = models.ForeignKey(
        Order,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='lineitems'
    )

    # Link to the product being purchased
    product = models.ForeignKey(
        Product,
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )

    # Optional size field for clothing items (XS, S, M, L, XL)
    product_size = models.CharField(
        max_length=2,
        null=True,
        blank=True
    )  # XS, S, M, L, XL

    # Number of units of this product in the order
    quantity = models.IntegerField(
        null=False,
        blank=False,
        default=0
    )

    # Total cost for this line item — calculated automatically on save
    # editable=False prevents manual changes in the admin
    lineitem_total = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=False,
        blank=False,
        editable=False
    )

    def save(self, *args, **kwargs):
        """
        Override the default save method to automatically calculate
        the line item total (product price * quantity) before saving.
        Also triggers update_total() on the parent order to keep
        the order grand total accurate.
        """
        # Calculate line item total from product price and quantity
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

         # Update the parent order totals to reflect this line item
        self.order.update_total()

    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'
