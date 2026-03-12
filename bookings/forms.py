from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'class_type',
            'class_date',
            'class_time',
            'duration',
            'trainer_name',
        ]
