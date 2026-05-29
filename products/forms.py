from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Category


SIZE_CHOICES = (
    ('xs', 'XS'),
    ('s', 'S'),
    ('m', 'M'),
    ('l', 'L'),
    ('xl', 'XL'),
)


class ProductForm(forms.ModelForm):

    image = forms.ImageField(
        label='Image',
        required=False,
        widget=CustomClearableFileInput()
    )

    sizes = forms.ChoiceField(
        choices=[('', 'Select Size')] + list(SIZE_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'size-select'})
    )

    class Meta:
        model = Product
        fields = '__all__'


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        categories = Category.objects.all()

        friendly_names = [
            (c.id, c.get_friendly_name())
            for c in categories
        ]

        self.fields['category'].choices = [
            ('', 'Select Category')
        ] + friendly_names

        placeholders = {
            'name': 'Product Name',
            'description': 'Product Description',
            'price': 'Price',
            'image_url': 'Image URL',
        }

        for field_name, field in self.fields.items():

            field.label = False
            field.widget.attrs['class'] = 'rounded'

            if field_name in placeholders and field.widget.input_type in ['text', 'number', 'textarea', 'email']:
                field.widget.attrs['placeholder'] = placeholders[field_name]

    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.cleaned_data.get('sizes'):
            instance.sizes = self.cleaned_data['sizes']

        if commit:
            instance.save()

        return instance

    