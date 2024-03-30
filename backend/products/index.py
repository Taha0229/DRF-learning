from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from .models import Product

@register(Product)  ## can understand it like registering to admin sites: admin.site.register(Product, ProductManagerAdmin)
class ProductIndex(AlgoliaIndex):
    # should_index = 'is_public'
    fields=[
        'title',
        'body',
        'price',
        'user',
        'public',
        'path',
        'endpoint'
    ]
    settings = {
        "searchableAttributes" : ["title", "body"],
        "attributesForFaceting" : ["user", "public"]
    }
    tags = 'get_tags'