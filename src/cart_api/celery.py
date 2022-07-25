from __future__ import absolute_import

import logging
import os

from celery import Celery
from celery.signals import after_setup_logger, after_setup_task_logger
from django.conf import settings

logger = logging.getLogger(__name__)


@after_setup_logger.connect
def on_after_setup_logger(logger, *args, **kwargs):
    from json_log_formatter import VerboseJSONFormatter

    if settings.API_LOG_CELERY_JSON:
        formatter = VerboseJSONFormatter()
        for handler in list(logger.handlers):
            handler.setFormatter(formatter)
            handler.setLevel(settings.API_LOG_CELERY_LEVEL)


@after_setup_task_logger.connect
def on_after_setup_task_logger(logger, *args, **kwargs):
    from json_log_formatter import VerboseJSONFormatter

    if settings.API_LOG_CELERY_JSON:
        formatter = VerboseJSONFormatter()
        for handler in list(logger.handlers):
            handler.setFormatter(formatter)
            handler.setLevel(settings.API_LOG_CELERY_LEVEL)


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cart_api.settings')

celery_app = Celery('cart_api')

celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()

celery_app.conf.broker_transport_options = settings.CELERY_BROKER_TRANSPORT_OPTIONS


@celery_app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
    return 42
