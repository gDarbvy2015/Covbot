import logging
import sys


class Formatter(logging.Formatter):
    grey: str = "\x1b[38;20m"
    yellow: str = "\x1b[33;20m"
    red: str = "\x1b[31;20m"
    bold_red: str = "\x1b[31;1m"
    reset: str = "\x1b[0m"
    format: str = "%(asctime)s %(levelname)s - %(module)s: %(message)s"

    FORMATS: dict = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno)
        formatter: logging.Formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class Logger(logging.Logger):
    def __init__(self, name: str):
        super().__init__(name)

        stream_handler: logging.StreamHandler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.INFO)

        stream_handler.setFormatter(Formatter())

        self.addHandler(stream_handler)