import logging
import os
import pathlib
from logging.handlers import TimedRotatingFileHandler
import sys


server_log_format: str = "%(asctime)s %(levelname)s - %(module)s: %(message)s"
log_path: pathlib.Path = pathlib.Path(os.environ.get("COVBOT_LOGS"))


class ColoredFormatter(logging.Formatter):
    """A formatter that allows printing logs in color using the custom output format."""

    grey: str = "\x1b[38;20m"
    yellow: str = "\x1b[33;20m"
    red: str = "\x1b[31;20m"
    bold_red: str = "\x1b[31;1m"
    reset: str = "\x1b[0m"

    FORMATS: dict = {
        logging.DEBUG: grey + server_log_format + reset,
        logging.INFO: grey + server_log_format + reset,
        logging.WARNING: yellow + server_log_format + reset,
        logging.ERROR: red + server_log_format + reset,
        logging.CRITICAL: bold_red + server_log_format + reset
    }

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno)
        formatter: logging.Formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class Formatter(logging.Formatter):
    """A formatter that allows printing logs using the custom output format."""
    def format(self, record: logging.LogRecord) -> str:
        formatter: logging.Formatter = logging.Formatter(server_log_format)
        return formatter.format(record)


class ServerLogger(logging.Logger):
    """Logger that can be used by the Flask webserver to log important information."""
    def __init__(self, name: str):
        super().__init__(name)

        rotating_file_handler: TimedRotatingFileHandler = TimedRotatingFileHandler(log_path / "server_log", "D")
        rotating_file_handler.setLevel(logging.INFO)

        stream_handler: logging.StreamHandler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.INFO)

        stream_handler.setFormatter(ColoredFormatter())
        rotating_file_handler.setFormatter(Formatter())

        self.addHandler(stream_handler)
        self.addHandler(rotating_file_handler)


class MessageLogger(logging.Logger):
    """Logger that can be used to log the queries and their response."""
    def __init__(self, name: str):
        super().__init__(name)

        file_handler: logging.FileHandler = logging.FileHandler(log_path / "messages_log")
        file_handler.setLevel(logging.INFO)

        file_handler.setFormatter(Formatter())

        self.addHandler(file_handler)