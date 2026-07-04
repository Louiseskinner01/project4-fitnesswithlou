from django.db import models


class Category(models.Model):
    """
    Stores a product category.
    Used to group and filter products on the products page.
    Each product belongs to one category via a ForeignKey.
    """

    class Meta:
        # Override the default plural name in Django admin
        # to display 'Categories' instead of 'Categorys'
        verbose_name_plural = "Categories"

    # Internal category name used for filtering and URL parameters
    name = models.CharField(max_length=254)

    # Human readable category name displayed to users
    # Optional — falls back to name if not provided
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        """Return the human readable category name for display in templates"""
        return self.friendly_name


class Product(models.Model):
    """
    Stores a single product in the FWL store.
    Contains all product information including name, description,
    price, category, available sizes and product image.
    Images are uploaded to Cloudinary via the ImageField.
    """

    # Product display name shown throughout the site
    name = models.CharField(max_length=100)

    # Brief product description displayed on the product detail page
    description = models.CharField(max_length=100)

    # Comma separated list of available sizes for clothing items
    # e.g. 'xs,s,m,l,xl' — blank if the product has no sizes
    sizes = models.CharField(
        max_length=50,
        blank=True,
        help_text="Comma separated sizes e.g. s,m,l,xl"
    )

    # Product price in GBP
    price = models.DecimalField(max_digits=6, decimal_places=2)

    # Link to the product's category
    # SET_NULL allows products to remain if their category is deleted
    # null and blank allow products to exist without a category
    category = models.ForeignKey(
        'Category',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    # Product image uploaded to Cloudinary via django-cloudinary-storage
    # blank=True allows products to be created without an image
    image = models.ImageField(upload_to='products/', blank=True)

    def __str__(self):
        return self.name
