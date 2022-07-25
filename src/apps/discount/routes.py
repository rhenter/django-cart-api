from rest_framework.routers import DefaultRouter

from .views import DiscountCouponViewSet

app_name = "discount"

router = DefaultRouter()

router.register(r'coupons', DiscountCouponViewSet, basename='coupons')

urlpatterns = router.urls
