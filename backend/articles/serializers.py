from rest_framework import serializers
from .models import Article
from products import validators
from api.serializers import UserPublicArticleSerializer

class ArticleSerializer(serializers.ModelSerializer):
    author = UserPublicArticleSerializer(source="user", read_only=True)
    title = serializers.CharField(validators=[validators.validate_title_no_title, validators.unique_product_title])
    public = serializers.BooleanField(source="make_public")
    endpoint = serializers.HyperlinkedIdentityField(view_name="article-detail", lookup_field="pk")

    class Meta:
        model = Article
        fields = ["pk", "author", "title", "body", "path","endpoint", "public", "tags"]
        
        
    def create(self, validated_data):
        obj = super().create(validated_data)
        return obj
        
        