from rest_framework import serializers



class UserProductInlineSerializer(serializers.Serializer):       

    url = serializers.HyperlinkedIdentityField(view_name="product-detail", lookup_field="pk", read_only=True )
    title = serializers.CharField(read_only=True)
    custom_field = serializers.SerializerMethodField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    
    def get_custom_field(self, obj):
        return f"can put anything in this custom field {obj.id}"
    
class UserPublicSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    other_products = serializers.SerializerMethodField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    
    def get_other_products(self, obj):
        user = obj
        # print("self: ", self)
        # print("c_id: ", user.product_set.values("id")[:5])
        my_products_qs = user.product_set.all()[:5]
        return UserProductInlineSerializer(my_products_qs, many=True, context=self.context).data
    
    
    
    
        
class UserPublicArticleSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    # this_is_not_real = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)