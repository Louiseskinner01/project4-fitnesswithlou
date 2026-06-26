from allauth.account.forms import LoginForm
from crispy_forms.helper import FormHelper


class CustomLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Hide labels
        self.fields['login'].label = False
        self.fields['password'].label = False

        # Add placeholders
        self.fields['login'].widget.attrs['placeholder'] = 'Email Address'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'

        # Add classes
        self.fields['login'].widget.attrs['class'] = 'form-control auth-input'
        password_widget = self.fields['password'].widget.attrs
        password_widget['class'] = 'form-control auth-input'
        self.helper = FormHelper()
