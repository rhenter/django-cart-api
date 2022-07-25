import json
import os
import sys
import urllib
from urllib.parse import quote

import ddtrace
import sentry_sdk
from corsheaders.defaults import default_headers
from dj_database_url import parse as parse_db_url
from django.core.management.utils import get_random_secret_key
from django_cache_url import parse as parse_cache_url
from kombu import Exchange, Queue
from kombu.utils.url import safequote
from prettyconf import config
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from unipath import Path

from .logging import get_datadog_logging_config, get_loggers, get_sentry_logging_config
from .utils import get_version

# Project Structure
BASE_DIR = Path(__file__).ancestor(3)
PROJECT_DIR = Path(__file__).ancestor(2)
FRONTEND_DIR = PROJECT_DIR.child("frontend")
SETTINGS_FOLDER = 'cart_api'

# App version
APP_VERSION = '0.1.0'
APP_NAME = config("APP_NAME", default='Cart API')

# Developer Info
DEVELOPER_NAME = config("DEVELOPER_NAME", default='Cart API')
DEVELOPER_WEBSITE = config("DEVELOPER_WEBSITE", default='')

WEBSITE = config("WEBSITE", default=f'car-api.local')

# Debug & Development
DEBUG = config("DEBUG", default=False, cast=config.boolean)

# Database
default_dburl = 'sqlite:///{}/db.sqlite3'.format(PROJECT_DIR)

REPLICA_DATABASES = config("REPLICA_DATABASES", default=[], cast=config.list)

if not REPLICA_DATABASES:
    DATABASES = {
        'default': config('DATABASE_URL', default=default_dburl, cast=parse_db_url),
    }
else:
    DATABASES = {
        'default': config('DATABASE_URL', default=default_dburl, cast=parse_db_url),
    }

    for i, replica_database_url in enumerate(REPLICA_DATABASES, 1):
        DATABASES[f'replica_{i}'] = parse_db_url(replica_database_url)


DATABASES['default']['TEST'] = {'NAME': config('TEST_DATABASE_NAME', default=None)}

DEFAULT_DATABASE_KEY = 'default'

#  Security & Signup/Signin
ADMIN_USERNAME = config('ADMIN_USERNAME', default='admin')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*', cast=config.list)
SECRET_KEY = config('SECRET_KEY', default=get_random_secret_key())
#  Media & Static
MEDIA_URL = "/media/"
MEDIA_ROOT = config('MEDIA_ROOT', default=FRONTEND_DIR.child("media"))

STATIC_URL = config('STATIC_URL', default='/static/')
STATIC_ROOT = config(
    'STATIC_ROOT', default=str(PROJECT_DIR.child('staticfiles'))
)

STATICFILES_DIRS = [
    FRONTEND_DIR.child("static"),
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
)

# Media Files
USE_S3_BACKEND = config('USE_S3_BACKEND', default=False, cast=bool)
ASSESTS_STORAGE_ROOT = config('ASSESTS_STORAGE_ROOT', default='assets/')
DOCUMENTS_STORAGE_ROOT = config('DOCUMENTS_STORAGE_ROOT', default='documents/')
IMAGES_STORAGE_ROOT = config('IMAGES_STORAGE_ROOT', default='images/')

# Storage
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# Backend Storage AWS S3
if USE_S3_BACKEND:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', default='')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', default='')
AWS_REGION_NAME = config('AWS_REGION_NAME', default='us-east-2')

AWS_DEFAULT_ACL = None
AWS_STORAGE_BUCKET_NAME = config('S3_AWS_STORAGE_BUCKET_NAME', default='hydrostats')
AWS_LOCATION = config('AWS_LOCATION', default='')
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_QUERYSTRING_EXPIRE = '3600'

AWS_CONFIG = {
    'aws_access_key_id': AWS_ACCESS_KEY_ID,
    'aws_secret_access_key': AWS_SECRET_ACCESS_KEY,
    'region_name': AWS_REGION_NAME
}

AWS_S3_REGION_NAME = AWS_REGION_NAME
AWS_S3_SIGNATURE_VERSION = 's3v4'

AWS_S3_HOST = AWS_REGION_NAME
S3_USE_SIGV4 = True

# Application definition
INSTALLED_APPS = (
    'clearcache',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 3rd party libs
    'django_filters',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_yasg',
    'oauth2_provider.apps.DOTConfig',
    'django_models',
    'django.forms',
    'rest_condition',
    'django_extensions',
    # Local
    'apps.core.apps.CoreConfig',
    'apps.user.apps.UserConfig',
    'apps.discount.apps.DiscountConfig',
    'apps.product.apps.ProductConfig',
    'apps.cart.apps.CartConfig',

)

MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = '{}.urls'.format(SETTINGS_FOLDER)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (
            FRONTEND_DIR.child("templates"),
        ),
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': config(
                "TEMPLATE_DEBUG",
                default=DEBUG,
                cast=config.boolean),
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.context_processors.environment_info',
            ],
        },
    },
]
FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

WSGI_APPLICATION = f'{SETTINGS_FOLDER}.wsgi.application'

AUTHENTICATION_BACKENDS = (
    'apps.core.backends.MultipleLoginModelBackend',
    'oauth2_provider.backends.OAuth2Backend',
    'django.contrib.auth.backends.ModelBackend'
)

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGES = (
    ("pt-br", "Português (Brasil)"),
    ("en", "English"),
)
LANGUAGE_CODE = 'en'
LOCALE_PATHS = (
    PROJECT_DIR.child("locale"),
)

DECIMAL_SEPARATOR = ','
USE_THOUSAND_SEPARATOR = True


CORS_ALLOW_ALL_ORIGINS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = (
    "accept",
    "accept-encoding",
    "accept-timezone",
    "access-control-allow-headers",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "x-timezone",
)

LOGIN_URL = "/"
LOGOUT_URL = "/logout/"
LOGIN_REDIRECT_URL = "/doc/"

# Logging
API_LOG_CELERY_JSON = config("API_LOG_CELERY_JSON", default=True, cast=config.boolean)
API_LOG_ROOT = config("API_LOG_ROOT", default='')

LOG_LEVEL = config("LOG_LEVEL", default="INFO")
LOG_FILE_SAVE = config("LOG_FILE_SAVE", default=False, cast=config.boolean)
LOG_PATH = config("LOG_PATH", default="/tmp")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}

SENTRY_DSN_URL = config("SENTRY_DSN_URL", default='')
if SENTRY_DSN_URL:
    LOGGING = get_sentry_logging_config()
    sentry_sdk.init(
        dsn=SENTRY_DSN_URL,
        integrations=[DjangoIntegration(), CeleryIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True,
    )

# Datadog Logging Settings
USE_DATADOG = config("USE_DATADOG", default=False, cast=config.boolean)

API_LOG_APPLICATION_LEVEL = config("API_LOG_APPLICATION_LEVEL", default=LOG_LEVEL)
API_LOG_CELERY_LEVEL = config("API_LOG_CELERY_LEVEL", default='INFO')
API_LOG_ERROR_LEVEL = config("API_LOG_ERROR_LEVEL", default='ERROR')

if USE_DATADOG:
    LOGGING = get_datadog_logging_config()
    ddtrace.patch_all()

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# EMAIL Authentication Settings
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')

EMAIL_ADMIN = config("EMAIL_ADMIN", default='')

EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=config.boolean)
EMAIL_HOST = config("EMAIL_HOST", default='localhost')
EMAIL_PORT = config("EMAIL_PORT", default=25, cast=int)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default='')
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default='')
DEFAULT_FROM_EMAIL = config("FROM_EMAIL", default='Cart API <donotreply@gerdau.com>')

SEND_EMAIL_NOTIFICATION = config('SEND_EMAIL_NOTIFICATION', default=False, cast=config.boolean)
SEND_EMAIL_SUPPORT_NOTIFICATION = config('SEND_EMAIL_SUPPORT_NOTIFICATION', default=False, cast=config.boolean)

# Celery
CELERY_BROKER_URL = config('BROKER_URL', default='')
CELERY_BROKER_TRANSPORT = config('BROKER_TRANSPORT', default="redis")

CELERY_BROKER_TRANSPORT_OPTIONS = {
    'max_retries': 3,
    'visibility_timeout': 3600,
    "worker_enable_remote_control": False,
    'priority_steps': list(range(10)),
    'sep': ':',
    'queue_order_strategy': 'priority'
}

if CELERY_BROKER_TRANSPORT == 'sqs':
    aws_access_key = safequote(AWS_ACCESS_KEY_ID)
    aws_secret_key = safequote(AWS_SECRET_ACCESS_KEY)
    CELERY_BROKER_URL = f"sqs://{aws_access_key}:{aws_secret_key}@"

    CELERY_TASK_DEFAULT_QUEUE = config('CELERY_TASK_DEFAULT_QUEUE', default='')
    CELERY_BROKER_TRANSPORT_OPTIONS.update({
        'region': AWS_REGION_NAME,
        'polling_interval': 30,
    })

CELERY_RESULT_BACKEND = 'django-db'
CELERY_TASK_RESULT_EXPIRES = config('CELERY_TASK_RESULT_EXPIRES', default=4, cast=int)
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_REMOTE_CONTROL = False
CELERY_SEND_EVENTS = False
CELERY_ENABLE_UTC = True
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

HIGH_PRIORITY_QUEUE_NAME = 'highpriority'

CELERY_QUEUES = (
    Queue(
        'celery',
        Exchange('celery', type='direct'),
        routing_key='celery',
    ),
    Queue(
        HIGH_PRIORITY_QUEUE_NAME,
        Exchange(HIGH_PRIORITY_QUEUE_NAME, type='direct'),
        routing_key=HIGH_PRIORITY_QUEUE_NAME,
    ),
)

CELERY_DEFAULT_ROUTING_KEY = 'celery'
CELERY_DEFAULT_EXCHANGE_TYPE = 'direct'
CELERY_DEFAULT_QUEUE = 'celery'

# Swagger configs
SWAGGER_SETTINGS = {
    'SUPPORTED_SUBMIT_METHODS': ['get', 'post', 'put', 'delete', 'patch'],  # default
    'JSON_EDITOR': False,
    'SECURITY_DEFINITIONS': {
        'Token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        },
        'OAuth2 Token': {
            'type': 'oauth2',
            'authorizationUrl': '/o/authorize',
            'tokenUrl': '/o/login/',
            'flow': 'accessCode',
            'scopes': {
                'read:groups': 'read groups',
            }
        }
    },
    'OAUTH2_CONFIG': {
        'clientId': 'yourAppClientId',
        'clientSecret': 'yourAppClientSecret',
        'appName': 'your application name'
    },
    'LOGIN_URL': LOGIN_URL,
    'LOGOUT_URL': LOGOUT_URL,
}

REDOC_SETTINGS = {
    'NATIVE_SCROLLBARS': True,
}


# Django REST Framework

AUTH_USER_MODEL = "user.User"
DATE_FORMAT = '%d/%m/%Y'
DATETIME_FORMAT = 'iso-8601'
DATE_INPUT_FORMATS = (
    '%m/%d/%Y', '%d/%m/%Y', '%Y-%m-%d',
    '%m-%d-%Y', '%d-%m-%Y',
)
DATETIME_INPUT_FORMATS = [
    '%m/%d/%Y',  # '2006-10-25'
    '%Y-%m-%d',  # '2006-10-25'
    '%d/%m/%Y',  # '25/10/2006'
    '%Y-%m-%d %H:%M',  # '2006-10-25 14:30'
    '%d/%m/%Y %H:%M',  # '25/10/2006 14:30'
    '%d/%m/%Y %H:%M:%S',  # '25/10/2006 14:30:00'
    '%d/%m/%Y %H:%M:%S.%f',  # '25/10/2006 14:30:00.1234123'
    '%m/%d/%Y %H:%M',  # '10/25/2006 14:30'
    '%m/%d/%Y %H:%M:%S',  # '10/25/2006 14:30:00'
    '%m/%d/%Y %H:%M:%S %Z',  # '10/25/2006 14:30:00 UTC'
    '%m/%d/%Y %H:%M:%S %z',  # '10/25/2006 14:30:00 +0000'
    '%m/%d/%Y %H:%M:%S.%f',  # '10/25/2006 14:30:00.12332'
    'iso-8601',
]

REST_FRAMEWORK = {
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter'
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    "DATE_INPUT_FORMATS": DATE_INPUT_FORMATS,
    "DATE_FORMAT": DATE_FORMAT,
    "DATETIME_INPUT_FORMATS": DATETIME_INPUT_FORMATS
}

CACHES = {
    'default': config('CACHE_URL', default='redis://localhost', cast=parse_cache_url)
}

APPEND_SLASH = True

CACHED_SERIALIZER_TIMEOUT = config(
    'CACHED_SERIALIZER_TIMEOUT',
    default='120',
    cast=config.eval)

DATA_UPLOAD_MAX_NUMBER_FIELDS = 20240

# This value is in minutes
ACTIVATE_CODE_EXPIRATION = config(
    'ACTIVATE_CODE_EXPIRATION',
    default='3',
    cast=config.eval)

CKEDITOR_BASEPATH = STATIC_URL + "ckeditor/ckeditor/"
CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        # 'skin': 'office2013',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'forms',
             'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                       'HiddenField']},
            '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert',
             'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'about', 'items': ['About']},
            '/',  # put this to force next toolbar on new line
            {'name': 'yourcustomtools', 'items': [
                # put the name of your editor.ui.addButton here
                'Preview',
                'Maximize',

            ]},
        ],
        'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
        # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
        # 'height': 291,
        # 'width': '100%',
        # 'filebrowserWindowHeight': 725,
        # 'filebrowserWindowWidth': 940,
        # 'toolbarCanCollapse': True,
        # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage',  # the upload image feature
            # your extra plugins here
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            # 'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
        'FormatOutput': False
    }
}

# Integrations
# Authentication: OAuth2
OAUTH2_PROVIDER = {
    'SCOPES': {
        'read': 'Read scope',
        'write': 'Write scope',
        'groups': 'Access to your groups'
    },
    # Default 20 days
    'ACCESS_TOKEN_EXPIRE_SECONDS': config('ACCESS_TOKEN_EXPIRE_SECONDS', default=1728000),
    # Default 30 days
    'REFRESH_TOKEN_EXPIRE_SECONDS': config('REFRESH_TOKEN_EXPIRE_SECONDS', default=2592000),
}

# B Rules
TERMS_OF_USE_VERSION_CURRENT = 1

DRF_YASG_EXCLUDE_VIEWS = [
    'health_check',
]
