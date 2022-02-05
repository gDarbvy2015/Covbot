import logging
import sys


class Logger(logging.Logger):
    def __init__(self, name: str):
        super().__init__(name)

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s - %(module)s: %(message)s")
        stream_handler.setFormatter(formatter)

        self.addHandler(stream_handler)
