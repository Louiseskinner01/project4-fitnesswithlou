from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class ClassSession(models.Model):
    """
    Stores a single fitness class session.
    Each session has a type, trainer, date, time, duration
    and capacity. The booked_count tracks how many users
    have booked the session and is used to enforce capacity
    limits during the booking process.
    """

    # The type of fitness class e.g. HIIT, Yoga, Pilates
    class_type = models.CharField(max_length=100)

    # Name of the instructor leading the session
    trainer = models.CharField(max_length=100)

    # Date the class takes place
    class_date = models.DateField()

    # Time the class starts
    class_time = models.TimeField()

    # Duration of the class in minutes
    duration = models.PositiveIntegerField()

    # Maximum number of participants allowed in the session
    capacity = models.PositiveIntegerField(default=20)

    # Running count of how many users have booked this session
    # Incremented when a booking is made and decremented on cancellation
    # Used to prevent overbooking by comparing against capacity
    booked_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.class_type} - {self.class_date} {self.class_time}"


class Booking(models.Model):
    """
    Stores a single booking made by a user for a class session.
    Links a user to a ClassSession and tracks the booking status.
    Used to prevent duplicate bookings and enforce class capacity limits.
    """

    # Link to the user who made the booking
    # Uses AUTH_USER_MODEL for flexibility with custom user models
    # CASCADE deletes the booking if the user account is deleted
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    # Link to the class session that was booked
    # CASCADE deletes the booking if the session is deleted
    session = models.ForeignKey(ClassSession, on_delete=models.CASCADE)

    # Current status of the booking
    # Defaults to 'booked' when a new booking is created
    booking_status = models.CharField(
        max_length=20,
        choices=[
            ('booked', 'Booked'),
            ('cancelled', 'Cancelled'),
            ('attended', 'Attended')
        ],
        default='booked'
    )

    # Automatically set to the date and time the booking was created
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.session}"
