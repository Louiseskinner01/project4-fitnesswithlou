from allauth.account.forms import LoginForm
from crispy_forms.helper import FormHelper


class CustomLoginForm(LoginForm):
    """
    Custom login form extending django-allauth's default LoginForm.
    Overrides the default form styling to match the FWL site design
    by removing labels, adding placeholder text and applying
    consistent CSS classes to the login and password fields.
    Uses crispy_forms FormHelper for enhanced form rendering.
    """

    def __init__(self, *args, **kwargs):
        """
        Customise the login form fields on initialisation.
        - Removes auto-generated labels from login and password fields
        - Adds descriptive placeholder text to each field
        - Applies consistent CSS styling to match the site's auth card design
        - Initialises crispy_forms FormHelper for improved form layout
        """
        super().__init__(*args, **kwargs)

        # Remove labels — placeholder text is used instead for cleaner UI
        self.fields['login'].label = False
        self.fields['password'].label = False

        # Add placeholder text to guide the user
        self.fields['login'].widget.attrs['placeholder'] = 'Email Address'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'

        # Apply consistent CSS classes to match the auth card styling
        self.fields['login'].widget.attrs['class'] = 'form-control auth-input'

        # Use a variable to avoid line length issues when setting
        # the password field's widget attributes
        password_widget = self.fields['password'].widget.attrs
        password_widget['class'] = 'form-control auth-input'

        # Initialise crispy_forms helper for enhanced form rendering
        self.helper = FormHelper()
