import logging
import warnings

from django.conf import settings

warnings.simplefilter("default")

logger = logging.getLogger(__name__)


def get_loggers(level, loggers):
    # logging.addLevelName("DISABLED", logging.CRITICAL + 10)

    default_handlers = ["console"]

    log_config = {
        "handlers": default_handlers,
        "level": level,
    }

    if level == "DISABLED":
        loggers = {
            "": {
                "handlers": ["null"],
                "level": "DEBUG",
                "propagate": False}}
    else:
        loggers = {log.strip(): log_config for log in loggers}

    loggers.update({
        "parso": {
            "propagate": False,
        }
    })

    return loggers


def get_sentry_logging_config(loggers=None):
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s %(levelname)s %(name)s:%(lineno)s %(message)s",
            },
            "json": {"()": "json_log_formatter.JSONFormatter"},
            "verbose_json": {"()": "json_log_formatter.VerboseJSONFormatter"},
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
            "null": {
                "class": "logging.NullHandler",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["console"],
                "level": settings.LOG_LEVEL,
                "propagate": True
            }
        },
    }

    if settings.LOG_FILE_SAVE:
        logging_config["handlers"] = {
            "json_file": {
                "class": "logging.FileHandler",
                "filename": f"{settings.LOG_PATH}/celery.log",
                "formatter": "json",
            }
        }
        logging_config["loggers"]["django"]["handlers"] = ["json_file"]

    return logging_config


def get_datadog_logging_config():
    if logger.hasHandlers():
        logger.handlers.clear()

    default_handlers = ["console"]
    if settings.LOG_FILE_SAVE:
        default_handlers = ["console", "json_file"]

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console": {"format": "{levelname} {message}", "style": "{"},
            "json": {"()": "json_log_formatter.JSONFormatter"},
            "verbose_json": {"()": "json_log_formatter.VerboseJSONFormatter"},
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "json"
            },
            "null": {
                "class": "logging.NullHandler",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["console"],
                "level": settings.LOG_LEVEL,
                "propagate": True
            }
        },
    }

    if settings.LOG_FILE_SAVE:
        logging_config["handlers"] = {
            "json_file": {
                "class": "logging.FileHandler",
                "filename": f"{settings.LOG_PATH}/celery.log",
                "formatter": "json",
            }
        }
        logging_config["loggers"]["django"]["handlers"] = ["json_file"]

    return logging_config
