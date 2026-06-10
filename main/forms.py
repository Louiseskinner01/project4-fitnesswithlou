from django import forms
from .models import NewsletterSignup

# Collect user data for News letter sign-up
class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSignup
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email address',
            })
        }