from django import forms

from .models import Product


class ProductForm(forms.ModelsFrom):
    class Meta:
        model = Product
        fields = (
            "pk",
            "title",
            "content",
            "price",
        )
