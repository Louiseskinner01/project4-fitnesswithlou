from django import forms
from .models import UserProfile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'fitness_goal',
            'experience_level',
            'preferred_training_time',
        ]
