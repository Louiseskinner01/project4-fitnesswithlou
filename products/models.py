from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/', blank=True)

    def __str__(self):
        return self.name