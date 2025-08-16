# myapp/forms.py
from django import forms
from core.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['seller', 'addedOn', 'updatedOn']
        
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'min': 0}),
            'stock': forms.NumberInput(attrs={'min': 0}),
            'password': forms.PasswordInput(render_value=True),
        }
