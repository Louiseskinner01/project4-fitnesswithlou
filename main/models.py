from django.db import models

# News letter sign-up
class NewsletterSignup(models.Model):
    email = models.EmailField(unique=True)
    date_signed_up = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class JobApplication(models.Model):
    POSITION_CHOICES = [
        ('', 'Select a job role...'),
        ('marketing', 'Marketing'),
        ('fitness_coach', 'Fitness Coach'),
        ('sales', 'Sales'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    position = models.CharField(max_length=50, choices=POSITION_CHOICES, default='')
    cv = models.FileField(upload_to='cvs/', null=True, blank=True)
    date_applied = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.position}"