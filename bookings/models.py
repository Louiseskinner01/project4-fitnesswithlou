from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
class ClassSession(models.Model):
    class_type = models.CharField(max_length=100)
    trainer = models.CharField(max_length=100)
    class_date = models.DateField()
    class_time = models.TimeField()
    duration = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField(default=20)
    booked_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.class_type} - {self.class_date} {self.class_time}"


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session = models.ForeignKey(ClassSession, on_delete=models.CASCADE)

    booking_status = models.CharField(
        max_length=20,
        choices=[
            ('booked', 'Booked'),
            ('cancelled', 'Cancelled'),
            ('attended', 'Attended')
        ],
        default='booked'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.session}"