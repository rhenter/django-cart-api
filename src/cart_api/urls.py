from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, re_path as url
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from apps.core.views.base import CustomLoginView
from apps.core.views.login import UserLoginDRFTokenView
from .schema import CustomOpenAPISchemaGenerator
from .utils import get_version


schema_view = get_schema_view(
    openapi.Info(
        title=settings.APP_NAME,
        default_version=get_version() or 'v1',
        description="Backend API from Cart",
        terms_of_service=f"{settings.WEBSITE}/terms-of-service/",
        contact=openapi.Contact(email=settings.EMAIL_ADMIN),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    # authentication_classes=(SessionAuthentication,),
    permission_classes=(permissions.AllowAny,),
    generator_class=CustomOpenAPISchemaGenerator
)

urlpatterns = [
    url(r'^$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    url(r'login/', CustomLoginView.as_view(), name='login'),
    url(r'logout/', auth_views.logout_then_login, name='logout'),

    # Auth
    url(r'^v1/auth-login/', UserLoginDRFTokenView.as_view()),
]

urlpatterns += i18n_patterns(
    url(r'^doc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    url('^admin/clearcache/', include('clearcache.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

    url(r'password_reset/', auth_views.PasswordResetView.as_view(
        html_email_template_name='registration/password_reset_email.html',
    ), name='password_reset'),
    url(r'password_reset/done/$', auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'),
    url(r'reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    url(r'reset/done/$', auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'),
)

api_urlpatterns = [
    url(r"^v1/core/", include("apps.core.urls", namespace='core')),
    url(r"^v1/cart/", include("apps.cart.routes", namespace='cart')),
    url(r"^v1/discount/", include("apps.discount.routes", namespace='discount')),
    url(r"^v1/product/", include("apps.product.routes", namespace='product')),
    url(r"^v1/user/", include("apps.user.routes", namespace='user')),
]

urlpatterns.extend(api_urlpatterns)
