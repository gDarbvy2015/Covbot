from enum import Enum


class Topic(Enum):
    SINGLE_TOPIC = 1
    MULTIPLE_TOPICS = 2
    NOT_SPECIFIED = 3


class Area(Enum):
    ONE_COUNTRY = 1
    MANY_COUNTRIES = 2
    NOT_SPECIFIED = 3
    WORLDWIDE = 4


class TimeFrame(Enum):
    SINGLE_DAY = 1
    TIME_FRAME = 2
    NOT_SPECIFIED = 3


class Datapoint(Enum):
    NUMBER = 1
    MAXIMUM = 3
    MINIMUM = 4
    DATE = 5
    NOT_SPECIFIED = 6


class Intent:
    def __init__(self, topic: Topic, area: Area, time_frame: TimeFrame, datapoint: Datapoint):
        self.topic = topic
        self.area = area
        self.time_frame = time_frame
        self.datapoint = datapoint
