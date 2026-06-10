from django.db import models

# News letter sign-up
class NewsletterSignup(models.Model):
    email = models.EmailField(unique=True)
    date_signed_up = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email