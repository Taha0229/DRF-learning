from rest_framework.routers import DefaultRouter

from products.viewsets import ProductViewSet

router = DefaultRouter()
router.register("product-abc", ProductViewSet, basename="products")
# print("from routers:", router.urls)
urlpatterns = router.urls