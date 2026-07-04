from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _

# Debug print statement to confirm the widget is loaded correctly
# Can be removed before final submission
print("CustomClearableFileInput loaded!")


class CustomClearableFileInput(ClearableFileInput):
    """
    Custom file input widget for product image uploads.
    Extends Django's built in ClearableFileInput widget to provide
    a customised image upload experience on the add and edit
    product forms.
    Overrides the default labels and uses a custom HTML template
    to display a thumbnail preview of the current product image
    alongside the file input, giving superusers a visual reference
    of the existing image before replacing it.
    The gettext_lazy function (_) is used for translation support
    allowing labels to be translated into other languages if needed.
    """

    # Label for the checkbox that removes the current image
    clear_checkbox_label = _('Remove')

    # Label displayed above the current image thumbnail
    initial_text = _('Current Image')

    # Label for the file input — set to empty string to hide it
    input_text = _('')

    # Path to the custom HTML template that renders the widget
    # Provides image preview functionality not available in the default widget
    template_name = (
        'products/custom_widget_template/custom_clearable_file_input.html'
    )
