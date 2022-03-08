import logging
from logging.handlers import TimedRotatingFileHandler
import sys


log_format: str = "%(asctime)s %(levelname)s - %(module)s: %(message)s"


class ColoredFormatter(logging.Formatter):

    grey: str = "\x1b[38;20m"
    yellow: str = "\x1b[33;20m"
    red: str = "\x1b[31;20m"
    bold_red: str = "\x1b[31;1m"
    reset: str = "\x1b[0m"

    FORMATS: dict = {
        logging.DEBUG: grey + log_format + reset,
        logging.INFO: grey + log_format + reset,
        logging.WARNING: yellow + log_format + reset,
        logging.ERROR: red + log_format + reset,
        logging.CRITICAL: bold_red + log_format + reset
    }

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno)
        formatter: logging.Formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class Formatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        formatter: logging.Formatter = logging.Formatter(log_format)
        return formatter.format(record)


class ServerLogger(logging.Logger):
    def __init__(self, name: str):
        super().__init__(name)

        rotating_file_handler: TimedRotatingFileHandler = TimedRotatingFileHandler("server_log", "M")
        rotating_file_handler.setLevel(logging.INFO)

        stream_handler: logging.StreamHandler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.INFO)

        stream_handler.setFormatter(ColoredFormatter())
        rotating_file_handler.setFormatter(Formatter())

        self.addHandler(stream_handler)
        self.addHandler(rotating_file_handler)
