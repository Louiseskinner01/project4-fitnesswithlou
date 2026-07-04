from django import forms
from .models import UserProfile


class ProfileForm(forms.ModelForm):
    """
    Form for viewing and updating the user's default delivery information.
    Based on the UserProfile model and only includes delivery related fields.
    Stripe fields and fitness preference fields are excluded as these
    are managed programmatically and not directly editable by the user.
    Used on the profile page to allow users to save their delivery
    details for faster checkout on future orders.
    """

    class Meta:
        model = UserProfile

        # Only include default delivery fields
        # Stripe IDs and fitness preference fields are excluded
        # as they are managed by the application not the user
        fields = (
            'default_phone_number',
            'default_street_address1',
            'default_street_address2',
            'default_town_or_city',
            'default_postcode',
            'default_country',
        )
