from django.db import models

# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=254)

    def __str__(self):
         return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to='products/', blank=True)

    def __str__(self):
        return self.name