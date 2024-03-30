from rest_framework import generics, mixins
from .models import Article
from .serializers import ArticleSerializer
from rest_framework.response import Response
from api.mixins import (UserQuerysetMixin, StaffEditorPermissionMixin)



class ArticleDetailAPIView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

article_detail_view = ArticleDetailAPIView.as_view()



class ArticleListCreateAPIView(StaffEditorPermissionMixin, UserQuerysetMixin, generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    allow_staff_view = False #comes  from StaffEditorPermissionMixin

    def perform_create(self, serializer):
        print("utilizing list create api")
        title = serializer.validated_data.get("title")
        body = serializer.validated_data.get("body")
        
        if body is None:
            body = title
        serializer.save( user=self.request.user, body=body)


article_list_create_view = ArticleListCreateAPIView.as_view()


class ArticleUpdateAPIView(generics.UpdateAPIView, StaffEditorPermissionMixin):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = "pk"

    def perform_update(self, serializer):
        instance = serializer.save()
        # extra logic if required
        if instance.body is None:
            instance.body = instance.title


article_update_view = ArticleUpdateAPIView.as_view()


class ArticleDestroyAPIView(generics.DestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = "pk"

    def perform_destroy(self, instance):
        # extra logic if required
        print(f"instance with article id {instance.id} is being deleted")
        super().perform_destroy(instance)


article_destroy_view = ArticleDestroyAPIView.as_view()



# implementing the FBV using CBV with the help of generic views + mixins


# class ProductMixinView(
#     UserQuerysetMixin,
#     generics.GenericAPIView,
#     mixins.ListModelMixin,
#     mixins.RetrieveModelMixin,
#     mixins.CreateModelMixin,
#     mixins.DestroyModelMixin,
# ):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     lookup_field = "pk"  # from RetrieveModelMixin
#     allow_staff_view = False #for UserQuerysetMixin
#     def get(
#         self, request, *args, **kwargs
#     ):  # this method is implemented from base class
#         pk = kwargs.get("pk")
#         if (
#             pk is not None
#         ):  # meaning that if some kwargs is passed or a parameter is passed to the request, then we will use the retrieve method
#             # but if no param is passed then we will simply return the list of all the data
#             return self.retrieve(request, *args, **kwargs)
#         # print("product_mixin_view is called")
#         return self.list(
#             self, request, *args, **kwargs
#         )  # the list method is implemented from the mixin class

#     def post(self, request, *args, **kwargs):
#         # print("post is triggered")
#         return self.create(request, *args, **kwargs)

#     def perform_create(self, serializer):
#         # perform extra operations
#         # print("perform create is triggered")
#         title = serializer.validated_data.get("title")
#         content = serializer.validated_data.get("content")
#         if content is None:
#             content = "from perform create"
#         serializer.save(content=content)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


# product_mixin_view = ProductMixinView.as_view()
