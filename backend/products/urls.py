from django.urls import path

from .views import *

# urlpatterns = [
#     path("", product_create_view),
#     path("<int:pk>/", product_detail_view)
# ]


urlpatterns = [
    path("", product_list_create_view, name="product-list"),
    # path("", product_alt_view),
    # path("", product_mixin_view),
    
    # path("<int:pk>/", product_detail_view),
    path("<int:pk>/", product_mixin_view, name="product-detail"),
    path("<int:pk>/update/", product_update_view, name="product-update"),
    # path("<int:pk>/delete/", product_destroy_view),
    path("<int:pk>/delete/", product_mixin_view, name="product-delete"),
]