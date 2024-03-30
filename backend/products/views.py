from rest_framework import generics, mixins
from .models import Product
from .serializers import ProductSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.mixins import (UserQuerysetMixin, StaffEditorPermissionMixin)



class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # def get(self, request, *args, **kwargs):
    #     pk = self.kwargs['pk']
    #     print("Primary Key:", pk)
    #     return super().get(request, *args, **kwargs)


product_detail_view = ProductDetailAPIView.as_view()


class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        # perform extra operations
        title = serializer.validated_data.get("title")
        content = serializer.validated_data.get("content")
        if content is None:
            content = title
        serializer.save(content=content)


product_create_view = ProductCreateAPIView.as_view()


class ProductListCreateAPIView(StaffEditorPermissionMixin, UserQuerysetMixin, generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    allow_staff_view = False

    def perform_create(self, serializer):
        print("utilizing list create api")
        # perform extra operations
        title = serializer.validated_data.get("title")
        # email = serializer.validated_data.pop("email")
        # print("email from views: ", email)
        
        content = serializer.validated_data.get("content")
        if content is None:
            content = title
        serializer.save( user=self.request.user, content=content)
        
    ## commented since we are using mixin instead of fxns     
    # def get_queryset(self, *args, **kwargs): #use args and kwargs when unsure about the params
    #     qs = super().get_queryset(*args, **kwargs)
    #     request = self.request
    #     user = request.user
    #     # if not user.is_authenticated:    #this can be done if permission mixin is not implemented
    #     #     return Product.objects.none()
    #     return qs.filter(user=request.user)


product_list_create_view = ProductListCreateAPIView.as_view()


class ProductUpdateAPIView(generics.UpdateAPIView, StaffEditorPermissionMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"

    def perform_update(self, serializer):
        instance = serializer.save()
        # extra logic if required
        if instance.content is None:
            instance.content = instance.title


product_update_view = ProductUpdateAPIView.as_view()


class ProductDestroyAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"

    def perform_destroy(self, instance):
        # extra logic if required
        print(f"instance with product id {instance.id} is being deleted")
        super().perform_destroy(instance)


product_destroy_view = ProductDestroyAPIView.as_view()


@api_view(["GET", "POST"])
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method
    if method == "GET":
        if pk is not None:
            obj = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(obj, many=False).data
            return Response(data)
        queryset = Product.objects.all()
        data = ProductSerializer(queryset, many=True).data
        return Response(data)

    if method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get("title")
            content = serializer.validated_data.get("content")
            if content is None:
                content = title
            serializer.save(content=content)
            return Response(serializer.data)
        return Response({"invalid": "not good data"}, status=400)


# implementing the FBV using CBV with the help of generic views + mixins


class ProductMixinView(
    UserQuerysetMixin,
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"  # from RetrieveModelMixin
    allow_staff_view = False #for UserQuerysetMixin
    def get(
        self, request, *args, **kwargs
    ):  # this method is implemented from base class
        pk = kwargs.get("pk")
        if (
            pk is not None
        ):  # meaning that if some kwargs is passed or a parameter is passed to the request, then we will use the retrieve method
            # but if no param is passed then we will simply return the list of all the data
            return self.retrieve(request, *args, **kwargs)
        # print("product_mixin_view is called")
        return self.list(
            self, request, *args, **kwargs
        )  # the list method is implemented from the mixin class

    def post(self, request, *args, **kwargs):
        # print("post is triggered")
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        # perform extra operations
        # print("perform create is triggered")
        title = serializer.validated_data.get("title")
        content = serializer.validated_data.get("content")
        if content is None:
            content = "from perform create"
        serializer.save(content=content)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


product_mixin_view = ProductMixinView.as_view()
