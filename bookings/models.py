from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Booking(models.Model):

    CLASS_CHOICES = [
        ('yoga', 'Yoga'),
        ('hiit', 'HIIT'),
        ('strength', 'Strength Training'),
        ('pilates', 'Mat Pilates'),
        ('core', 'Core Blast'),
        ('lbt', 'Legs Bums & Tums'),
    ]

    BOOKING_CHOICES = [
            ('booked', 'Booked'),
            ('cancelled', 'Cancelled'),
            ('attended', 'Attended')
        ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class_type = models.CharField(max_length=50, choices=CLASS_CHOICES)
    class_date = models.DateField()
    class_time = models.TimeField()
    duration = models.IntegerField(help_text="Class duration in minutes")
    trainer_name = models.CharField(max_length=100)
    max_capacity = models.IntegerField(default=15)
    booking_status = models.CharField(max_length=20, choices=BOOKING_CHOICES, 
        default='booked')

    Created_at = models.DateTimeField(auto_now_add=True)

def __str__(self):
    return f"{self.class_type} - {self.class_date}"