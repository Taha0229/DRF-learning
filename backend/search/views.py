from rest_framework import generics
from rest_framework.response import Response
from itertools import chain
from products.models import Product
from articles.models import Article
from products.serializers import ProductSerializer
from . import client

class SearchListView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        user = None
        if request.user.is_authenticated:
            user = request.user.username
        query = request.GET.get('q')
        public = str(request.GET.get('public')) != "0"
        tag = request.GET.getlist('tags') or None
        if not query:
            return Response('Please add a query', status=400)
        results = client.perform_query(query, tags=tag, user=user, public=public)
        return Response(results)
    
    def get_queryset(self):
        qs1 = Article.objects.all()
        qs2 = Product.objects.all()
        return chain(qs1, qs2)

class SearchListOldView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        q = self.request.GET.get('q')
        results = Product.objects.none()
        if q is not None:
            user = None
            if self.request.user.is_authenticated:
                user = self.request.user
            results = qs.search(q, user=user)
        return results