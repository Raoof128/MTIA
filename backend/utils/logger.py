"""Logging configuration utility."""

import logging
import sys

from colorama import Fore, Style, init

init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    """Custom formatter for colored log output."""

    FORMATS = {
        logging.DEBUG: Fore.CYAN
        + "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        + Style.RESET_ALL,
        logging.INFO: Fore.GREEN
        + "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        + Style.RESET_ALL,
        logging.WARNING: Fore.YELLOW
        + "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        + Style.RESET_ALL,
        logging.ERROR: Fore.RED
        + "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        + Style.RESET_ALL,
        logging.CRITICAL: Fore.RED
        + Style.BRIGHT
        + "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        + Style.RESET_ALL,
    }

    def format(self, record):
        """Format the log record with colors."""
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


def get_logger(name):
    """Get a configured logger instance."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(ColoredFormatter())
        logger.addHandler(console_handler)

    return logger
