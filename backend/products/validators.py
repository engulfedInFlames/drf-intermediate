from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Product


# def validate_title(value):
#     product = Product.objects.filter(title__iexact=value)
#     if product.exists():
#         raise serializers.ValidationError(f"Product name '{value}' already exists.")
#     return value


def validate_title_no_admin(value):
    if "admin" in value.lower():
        raise serializers.ValidationError(
            f"Product name cannot include case-insensitive 'admin'. "
        )
    return str(value)


validate_product_title_is_unique = UniqueValidator(
    queryset=Product.objects.all(),
    lookup="iexact",
)
