from django import forms
from .models import NewsletterSignup
from .models import JobApplication




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


# Collect user data for career enquiry
class JobApplicationForm(forms.ModelForm):

    cv = forms.FileField(required=False)
    class Meta:
        model = JobApplication
        fields = ['first_name', 'last_name', 'email', 'position', 'cv']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'name@example.com'}),
            'position': forms.Select(attrs={'class': 'form-control px-0'}),
            'cv': forms.FileInput(attrs={'id': 'id_cv', 'style': 'display:none;'}), 
        }