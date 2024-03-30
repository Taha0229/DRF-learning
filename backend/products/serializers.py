from rest_framework import serializers
from .models import Product
from rest_framework.reverse import reverse
from . import validators 
from api.serializers import UserPublicSerializer

class ProductSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(source="user", read_only=True)
    discount = serializers.SerializerMethodField(read_only=True, method_name="custom_get_discount")
    edit_url = serializers.SerializerMethodField(read_only=True)
    endpoint = serializers.HyperlinkedIdentityField(view_name="product-detail", lookup_field="pk")
    title = serializers.CharField(validators=[validators.validate_title_no_title, validators.unique_product_title])
    #extra tip
    name = serializers.CharField(source="title", read_only=True)
    email = serializers.EmailField(write_only=True)
    body = serializers.CharField(source="content")
    class Meta:
        model = Product
        fields = ["id", "public", "owner", "edit_url", "endpoint", "path" ,"title", "name", "email", "body", "price", "sale_price", "discount"]
        
    # def validate_title(self, value):
    #     request = self.context.get("request")
    #     # user = request.user
    #     # qs = Product.objects.filter(user=user, title__iexact=value)
    #     qs = Product.objects.filter(title__iexact=value)
    #     if qs.exists():
    #         raise serializers.ValidationError(f"{value} is already a product name") 
    #     return value
        
    def create(self, validated_data):
        email = validated_data.pop('email')
        print("email from serializer: ", email)
        obj = super().create(validated_data)
        return obj
        
    def custom_get_discount(self, obj):
        if not hasattr(obj, "id"):
            return None
        if not isinstance(obj, Product):
            return None
        return obj.get_discount()
        
    def get_edit_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("product-update", kwargs={"pk": obj.id}, request=request)
    
    # def get_name(self, obj):
    #     print("get_edit_url called")
    #     return "changed name"
    
