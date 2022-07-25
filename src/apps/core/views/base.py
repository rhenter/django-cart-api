import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView

logger = logging.getLogger(__name__)

User = get_user_model()


class CustomLoginView(LoginView):
    template_name = "login.html"
