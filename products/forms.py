from django import forms
from .models import Product, Category

class ProductfORM(forms.ModeForm):

    class Meta:
        model = Productfields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Categories = Category.object.all()
        friendly_names = [(c.id, c.get_friendly_names())
                            for c in Categories
                        ]
        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
