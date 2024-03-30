import json
from django.shortcuts import render
from django.http import JsonResponse
from products.models import Product
from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework.decorators import api_view
from products.serializers import ProductSerializer

# Create your views here.

# @api_view(["GET", "POST"])
# def api_home(request, *args, **kwargs):
#     data = request.data
#     print(data)
#     # instance = Product.objects.all().order_by("?").first()
#     # data = {}
#     # if instance:
#     #     # instance = model_to_dict(product, fields=["id", "title", "price", "sale_price", "discount"])
#     #     data = ProductSerializer(instance).data
    
#     return Response(data)

@api_view(["GET", "POST"])
### Data ingestional and validation

def api_home(request, *args, **kwargs):
    #Method - 1 without writing on the database
    
    # serializer = ProductSerializer(data=request.data)
    # if serializer.is_valid():
    #     print(serializer.data)
    #     data = serializer.data
    #     return Response(data)


#Method - 2: writing in the database

    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        instance = serializer.save()
        print(instance)
        return Response(serializer.data)
    return Response({"invalid": "Not good data"}, status=400)