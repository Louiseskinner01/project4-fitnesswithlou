from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Cart(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    # This is an example from chatGPT to help calculate the total price
    def get_cart_total(self):
        return sum(item.get_total_price() for item in self.items.all())

class CartItem(models.Model):  
    
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    # This is an example from chatGPT to help calculate the total price
    def get_total_price(self):
        return self.product * self.quantity