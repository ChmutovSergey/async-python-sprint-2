import os
import logging
from logging.config import dictConfig


LOG_LEVEL = "DEBUG"
DIR_NAME = os.path.join(os.path.dirname(os.path.realpath(__file__)), "logs")


def get_logger(logger_name: str, log_level: str = "INFO") -> logging.Logger:
    logger_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(filename)s:%(lineno)s - %(funcName)20s()] %(asctime)s %(message)s"
            },
        },
        "handlers": {
            "console": {
                "level": log_level,
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
            "file": {
                "level": log_level,
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "default",
                "filename": DIR_NAME + "/log_file.log",
                "maxBytes": 500000,
                "backupCount": 10
            }
        },
        "loggers": {
            "": {
                "handlers": ["file", "console"],
                "level": log_level,
                "propagate": False
            },
        }
    }

    dictConfig(logger_config)

    return logging.getLogger(logger_name)


logger = get_logger("root", LOG_LEVEL)
