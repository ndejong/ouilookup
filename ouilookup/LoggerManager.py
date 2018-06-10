
import os
import sys
import time
import logging


class LoggerManagerException(Exception):
    pass


class LoggerManager:

    date_format = '%Y%m%dZ%H%M%S'
    message_format = '%(asctime)s (%(levelname)s) %(name)s :: %(message)s'

    @staticmethod
    def build_logger(name, logfile=None, level=logging.INFO, is_console_debug=False, is_console_quiet=False):

        # Reference logging levels:-
        # https://docs.python.org/3/howto/logging.html#logging-levels
        #
        # CRITICAL  50
        # ERROR     40
        # WARNING   30
        # INFO      20
        # DEBUG     10
        # NOTSET    0

        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        logging.Formatter.converter = time.gmtime

        # logger_h1 = console logging
        logger_h1 = logging.StreamHandler(sys.stderr)
        if is_console_debug:
            logger_h1.setLevel(logging.DEBUG)
        else:
            if is_console_quiet:
                logger_h1.setLevel(logging.WARNING)
            else:
                logger_h1.setLevel(logging.INFO)
        logger_h1.setFormatter(logging.Formatter(datefmt=LoggerManager.date_format,fmt=LoggerManager.message_format))
        logger.addHandler(logger_h1)

        # logger_h2 = logfile logging
        if logfile is not None:
            if not os.path.isdir(os.path.dirname(logfile)):
                os.makedirs(os.path.dirname(logfile))
            logger_h2 = logging.FileHandler(logfile)
            logger_h2.setLevel(level)
            logger_h2.setFormatter(
                logging.Formatter(datefmt=LoggerManager.date_format, fmt=LoggerManager.message_format)
            )
            logger.addHandler(logger_h2)

        return logger


class LoggerNull:
    def __getattr__(self, __null):
        def __nully(*__nully):
            pass;
        return __nully
