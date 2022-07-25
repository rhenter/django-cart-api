from rest_framework.routers import DefaultRouter

from .views import CartViewSet, CartProductViewSet

app_name = "api-product"

router = DefaultRouter()

router.register(r'carts', CartViewSet, basename='carts')
router.register(r'cart-products', CartProductViewSet, basename='cart_products')

urlpatterns = router.urls
