from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Category


# Predefined size choices for clothing products
# Used in the sizes ChoiceField dropdown
SIZE_CHOICES = (
    ('xs', 'XS'),
    ('s', 'S'),
    ('m', 'M'),
    ('l', 'L'),
    ('xl', 'XL'),
)


class ProductForm(forms.ModelForm):
    """
    Form for adding and editing products in the FWL store.
    Used exclusively by superusers via the product management pages.
    Includes a custom image widget, size selector dropdown and
    dynamically populated category choices with friendly names.
    Labels are hidden and replaced with placeholder text for cleaner UI.
    """

    # Custom image field using the CustomClearableFileInput widget
    # which displays a thumbnail preview of the current image
    image = forms.ImageField(
        label='Image',
        required=False,
        widget=CustomClearableFileInput()
    )

    # Size selector dropdown with predefined clothing size choices
    # Prepends a blank 'Select Size' option for better UX
    sizes = forms.ChoiceField(
        choices=[('', 'Select Size')] + list(SIZE_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'size-select'})
    )

    class Meta:
        model = Product
        # Include all model fields in the form
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """
        Customise form fields on initialisation.
        - Replaces category IDs with friendly names in the dropdown
        - Adds placeholder text to text input fields
        - Applies consistent CSS styling to all fields
        - Removes auto-generated labels for cleaner appearance
        - Skips placeholder/label removal for the image field
          as it uses a custom widget
        """
        super().__init__(*args, **kwargs)

        # Retrieve all categories and build a list of
        # (id, friendly_name) tuples for the category dropdown
        categories = Category.objects.all()

        friendly_names = [
            (c.id, c.get_friendly_name())
            for c in categories
        ]

        # Replace the default category choices with friendly names
        # Prepends a blank 'Select Category' option
        self.fields['category'].choices = [
            ('', 'Select Category')
        ] + friendly_names

        # Placeholder text for text input fields
        placeholders = {
            'name': 'Product Name',
            'description': 'Product Description',
            'price': 'Price',
            'image_url': 'Image URL',
        }

        for field_name, field in self.fields.items():

            # Remove all field labels — placeholders are used instead
            field.label = False

            # Skip the image field as it uses a custom widget
            # that handles its own rendering
            if field_name == 'image':
                continue

            # Apply consistent rounded styling to all input fields
            field.widget.attrs['class'] = 'rounded'

            # Add placeholder text to text, number and email input types
            input_types = ['text', 'number', 'textarea', 'email']
            if (field_name in placeholders and
                    field.widget.input_type in input_types):
                field.widget.attrs['placeholder'] = (
                    placeholders[field_name]
                )

    def save(self, commit=True):
        """
        Override the default save method to handle the sizes field.
        The sizes field is a ChoiceField on the form but a CharField
        on the model. This method ensures the selected size value
        is correctly saved to the model instance before committing
        to the database.
        """
        # Create the model instance without saving to database yet
        instance = super().save(commit=False)

        # Save the selected size to the model instance
        if self.cleaned_data.get('sizes'):
            instance.sizes = self.cleaned_data['sizes']

        if commit:
            instance.save()

        return instance
