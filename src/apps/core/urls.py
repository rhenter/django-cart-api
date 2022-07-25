from django.urls import path

from . import views
from .views.http_status import page_not_found, unauthorized_access

app_name = 'core'

urlpatterns = [
    path('', views.CustomLoginView.as_view(), name="login"),

    # Error Pages
    path('401/', unauthorized_access, name='unauthorized_access'),
    path('404/', page_not_found, name='page_not_found'),
]
