from django import forms
from .models import Order
from django_countries.widgets import CountrySelectWidget


class OrderForm(forms.ModelForm):
    """
    Form for capturing customer delivery and contact details
    during the checkout process. Based on the Order model
    and excludes fields that are calculated automatically
    (such as order total and Stripe payment ID).
    """
    class Meta:
        model = Order
        # Only include fields the customer needs to fill in manually
        # Calculated fields like totals and stripe_pid are excluded
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'country',
                  )

    def __init__(self, *args, **kwargs):
        """
        Customise the form fields on initialisation.
        - Adds placeholder text to each field
        - Appends * to required field placeholders
        - Applies consistent CSS styling to all fields
        - Removes auto-generated labels (placeholders used instead)
        - Sets autofocus on the full name field for better UX
        """
        super().__init__(*args, **kwargs)
        
        # Placeholder text for each form field
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County',
        }

        # Set autofocus on the first field for better user experience
        self.fields['full_name'].widget.attrs['autofocus'] = True
        
        for field in self.fields:
            # Add asterisk to placeholder for required fields
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
                
            # Apply placeholder, CSS class and remove label for each field
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = ''
