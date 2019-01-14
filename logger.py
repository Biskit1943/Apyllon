"""Defines the logger for this service"""
import logging


class DoNotPropagate:
    """Provides a filter for the logs, so they are only logged on their level
    and do not propagate
    """

    def __init__(self, level):
        self.__level = level

    def filter(self, record):
        return record.levelno <= self.__level


logging_config = {
    'version': 1,
    'formatters': {
        'debug': {
            'class': 'logging.Formatter',
            'format': '%(levelname)-8s | %(asctime)s | %(name)s - %(message)s'
        },
        'info': {
            'class': 'logging.Formatter',
            'format': '%(levelname)-8s | %(message)s'
        },
        'warning': {
            'class': 'logging.Formatter',
            'format': '%(levelname)-8s | %(message)s'
        },
        'error': {
            'class': 'logging.Formatter',
            'format': '%(levelname)-8s | %(message)s'
        },
        'critical': {
            'class': 'logging.Formatter',
            'format': '%(levelname)-8s | %(message)s'
        },
    },
    'filters': {
        'do_not_propagate_info': {
            '()': DoNotPropagate,
            'level': logging.INFO,
        },
        'do_not_propagate_warning': {
            '()': DoNotPropagate,
            'level': logging.WARNING,
        },
        'do_not_propagate_error': {
            '()': DoNotPropagate,
            'level': logging.ERROR,
        },
        'do_not_propagate_critical': {
            '()': DoNotPropagate,
            'level': logging.CRITICAL,
        },
    },
    'handlers': {
        'debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '.logs',
            'mode': 'a+',
            'formatter': 'debug',
        },
        'info': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'info',
            'filters': [
                'do_not_propagate_info',
            ],
        },
        'warning': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'warning',
            'filters': [
                'do_not_propagate_warning',
            ],
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stderr',
            'formatter': 'error',
            'filters': [
                'do_not_propagate_error',
            ],
        },
        'critical': {
            'level': 'CRITICAL',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stderr',
            'formatter': 'critical',
            'filters': [
                'do_not_propagate_critical',
            ],
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['debug', 'info', 'warning', 'error', 'critical']
    },
}