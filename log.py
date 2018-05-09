"""Because you don't want camelCase in your code."""


__all__ = [
    'configure',
    'set_level',
    'log',
    'critical',
    'fatal',
    'error',
    'exception',
    'warning',
    'info',
    'debug',
]
__author__ = 'Carl Bordum Hansen'
__license__ = 'MIT'


import inspect
from functools import partial
import logging
from logging import CRITICAL, FATAL, ERROR, WARNING, INFO, DEBUG


def configure(**kwargs):
    """Alias for `logging.basicConfig`."""
    logging.basicConfig(**kwargs)


def set_level(logger, level):
    """Set output level of *logger* to *level*.

    Usage:
        set_level('requests', 'INFO')
    """
    logging.getLogger(logger).setLevel(level)


def log(level, msg, *args, **kwargs):
    """Log `*msg* % args` with severity *level*.

    To log exception information, use the keyword argument *exc_info* with a
    thruthy value.
    """
    module = inspect.currentframe().f_back.f_globals['__name__']
    logger = logging.getLogger(module)
    logger.log(level, msg, *args, **kwargs)


def exception(msg, *args, **kwargs):
    """Alias for `log.error(msg, *args, exc_info=True, **kwargs)`."""
    error(msg, *args, exc_info=True, **kwargs)


docstring = """\
Logs a *message* with level `{}`.

Args:
    message (str): the message to log.
    exc_info (bool): adds exception information to *message*. Default to False.

help(log) for more information about configuration.
"""

critical = partial(log, CRITICAL)
error = partial(log, ERROR)
warning = partial(log, WARNING)
info = partial(log, INFO)
debug = partial(log, DEBUG)

critical.__doc__ = docstring.format('CRITICAL')
error.__doc__ = docstring.format('ERROR')
warning.__doc__ = docstring.format('WARNING')
info.__doc__ = docstring.format('INFO')
debug.__doc__ = docstring.format('DEBUG')

fatal = critical
