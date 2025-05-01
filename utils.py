import logging
import hashlib
import pathlib

# Logging leverls: https://docs.python.org/3/library/logging.html#logging-levels
# 6 levels, from least to highest severity
# NOTSET < DEBUG < INFO < WARNING < ERROR < CRITICAL


def setup_logging(
    name="nobody",
    logger_loglevel=logging.DEBUG,
    file_handler_loglevel=logging.DEBUG,
    console_handler_loglevel=logging.DEBUG,
):
    """Setup logging at script level"""

    # create logs directory, if it doesn't exist
    log_dir = pathlib.Path("__file__").parent / ".logs"
    log_dir.mkdir(exist_ok=True)

    # configure logger
    logger = logging.getLogger(name=name)
    logger.setLevel(logger_loglevel)

    # write formatted logging records to log files
    file_handler = logging.FileHandler(log_dir / f"{name}.log")
    file_handler.setLevel(file_handler_loglevel)

    # write logging records to stream
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_handler_loglevel)

    # formatter
    # Cre: https://stackoverflow.com/a/49229328/9122512
    # log level to the front for better visual
    console_formatter = logging.Formatter(
        fmt="[%(levelname)s] %(name)s: func %(funcName)s[L%(lineno)d]: %(message)s\n",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_formatter = logging.Formatter(
        fmt="[%(levelname)s] %(asctime)s %(name)s: func %(funcName)s[L%(lineno)d]: %(message)s\n",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # add formatter to handler
    file_handler.setFormatter(file_formatter)
    console_handler.setFormatter(console_formatter)

    # add handler to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# A utility function that can be used in your code
# Cre: https://debugpointer.com/python/create-md5-hash-of-a-file-in-python
def compute_md5(file_name):
    hash_md5 = hashlib.md5()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
