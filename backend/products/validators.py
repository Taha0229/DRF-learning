from rest_framework import serializers
from .models import Product

from rest_framework.validators import UniqueValidator
 
 
def validate_title_no_title(value):
    if "title" in value.lower():
        raise serializers.ValidationError("title word is not allowed")
    return value

unique_product_title = UniqueValidator(queryset=Product.objects.all(), lookup="exact")