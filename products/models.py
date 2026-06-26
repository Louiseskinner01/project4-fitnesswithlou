from django.db import models

# Create your models here.


class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):

    name = models.CharField(max_length=100)
    description = models.CharField(
        max_length=100)
    sizes = models.CharField(
        max_length=50, blank=True,
        help_text="Comma separated sizes e.g. s,m,l,xl")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to='products/', blank=True)

    def __str__(self):
        return self.name
