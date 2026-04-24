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

        widgets = {
            'class_type': forms.Select(attrs={'class': 'form-control'}),
            'class_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'class_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'trainer_name': forms.TextInput(attrs={'class': 'form-control'}),
        }