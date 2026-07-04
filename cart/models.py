from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Cart(models.Model):
    """
    Stores a shopping cart for an authenticated user.
    Each user has one cart which persists between sessions.
    The cart contains multiple CartItem objects linked via
    the related_name 'items'.
    """

    # Link to the Django user who owns this cart
    # CASCADE deletes the cart if the user account is deleted
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Automatically set when the cart is first created
    created_at = models.DateTimeField(auto_now_add=True)

    # Automatically updated every time the cart is saved
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    def get_cart_total(self):
        """
        Calculate and return the total price of all items in the cart.
        Iterates through all cart items and sums their individual
        totals using the get_total_price method on each CartItem.
        """
        return sum(item.get_total_price() for item in self.items.all())


class CartItem(models.Model):
    """
    Stores a single product within a user's cart.
    Each cart item represents one product with a specific
    quantity and optional size. Multiple cart items can
    belong to the same cart.
    """

    # Link to the parent cart
    # CASCADE deletes the item if the cart is deleted
    # related_name='items' allows access via cart.items.all()
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        null=True,
        blank=True
    )

    # Link to the product being added to the cart
    # CASCADE removes the cart item if the product is deleted
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    # Number of units of this product in the cart
    quantity = models.PositiveIntegerField(default=1)

    # Price of the product at the time it was added to the cart
    # Stored separately to preserve the price if the product price changes
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    # Optional size for clothing items (e.g. XS, S, M, L, XL)
    # Null and blank as not all products have sizes
    size = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total_price(self):
        """
        Calculate and return the total price for this cart item.
        Multiplies the current product price by the quantity.
        Uses product.price rather than the stored price field
        to always reflect the current product price.
        """
        return self.product.price * self.quantity