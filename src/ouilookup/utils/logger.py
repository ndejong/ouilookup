import logging

__logging_format__ = "__name__ [%(levelname)s] %(message)s"
# __logging_format__ = "%(asctime)s | %(levelname)s | __name__ | %(message)s"
__logging_date_format__ = "%Y-%m-%dT%H:%M:%S%z"


def logger_get(name: str, loglevel="warning", logfile=None) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logging_level = __logger_level_int(loglevel)
    logger.setLevel(logging_level)

    logging_format = __logging_format__.replace("__name__", name)
    logging_formatter = logging.Formatter(fmt=logging_format, datefmt=__logging_date_format__)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging_level)
    console_handler.setFormatter(logging_formatter)

    logger.addHandler(console_handler)

    try:
        if logfile:
            file_handler = logging.FileHandler(filename=logfile)
            file_handler.setLevel(logging_level)
            file_handler.setFormatter(logging_formatter)
            logger.addHandler(file_handler)
    except (FileNotFoundError, PermissionError):
        raise PermissionError(f"Unable to write to logfile at: {logfile}")

    return logger


def logger_setlevel(name: str, loglevel: str) -> None:
    logger = logging.getLogger(name)
    logging_level = __logger_level_int(loglevel)

    logger.setLevel(logging_level)
    for handler in logger.handlers:
        handler.setLevel(logging_level)

    return None


def __logger_level_int(loglevel) -> int:
    logging_level = logging.getLevelName(loglevel.upper())
    try:
        int(logging_level)
    except ValueError:
        raise ValueError(f"Unknown loglevel requested: {loglevel}")

    return int(logging_level)
