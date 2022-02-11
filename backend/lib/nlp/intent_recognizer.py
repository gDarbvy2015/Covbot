from enum import Enum

class IntentRecognizer:
    def __init__(self):
        pass


class Topic(Enum):
    VACCINATION = 1
    POSITIVE_CASE = 2
    UNKNOWN = 3


class Intention(Enum):
    NEW_NUMBER = 1
    MAXIMUM = 2
    MINIMUM = 3