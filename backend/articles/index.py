from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from .models import Article

@register(Article)  ## can understand it like registering to admin sites: admin.site.register(Product, ProductManagerAdmin)
class ProductIndex(AlgoliaIndex):
    # should_index = 'public'
    fields=[
        'title',
        'body',
        'user',
        'publish_date',
        'public',
        'path',
        'endpoint'
    ]
    settings = {
        "searchableAttributes" : ["title", "body"],
        "attributesForFaceting" : ["user", "public"],
        "ranking": ['asc(publish_date)']
    }
    tags = 'get_tags_list'