from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from nltk import PorterStemmer
from spacy.tokens import Token

from lib.nlu.topic import TopicRecognizer, Topic


class CalculationType(Enum):
    RAW_VALUE = 1
    SUM = 2
    MAXIMUM = 3
    MINIMUM = 4
    UNKNOWN = 5

    @staticmethod
    def from_str(calculation_type: str) -> Optional[CalculationType]:
        try:
            return CalculationType[calculation_type.upper()]
        except KeyError:
            return CalculationType["UNKNOWN"]


class ValueType(Enum):
    NUMBER = 1
    DAY = 2
    LOCATION = 3
    UNKNOWN = 4

    @staticmethod
    def from_str(value_type: str) -> Optional[ValueType]:
        try:
            return ValueType[value_type.upper()]
        except KeyError:
            return ValueType["UNKNOWN"]


class ValueDomain(Enum):
    ADMINISTERED_VACCINES = 1
    VACCINATED_PEOPLE = 2
    POSITIVE_CASES = 3
    UNKNOWN = 4

    @staticmethod
    def from_str(value_domain: str) -> Optional[ValueDomain]:
        try:
            return ValueDomain[value_domain.upper()]
        except KeyError:
            return ValueDomain["UNKNOWN"]


class MeasurementType(Enum):
    DAILY = 1
    CUMULATIVE = 2
    UNKNOWN = 3

    @staticmethod
    def from_str(measurement_type: str) -> Optional[MeasurementType]:
        try:
            return MeasurementType[measurement_type.upper()]
        except KeyError:
            return MeasurementType["UNKNOWN"]


@dataclass
class Intent:
    calculation_type: CalculationType
    value_type: ValueType
    value_domain: ValueDomain
    measurement_type: MeasurementType


class IntentRecognizer:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.topic_recognizer = TopicRecognizer()

    def recognize_intent(self, token: Token) -> Optional[Intent]:

        value_domain = self.recognize_value_domain(token)

        return Intent(CalculationType.UNKNOWN, ValueType.UNKNOWN, value_domain, MeasurementType.UNKNOWN)
        # topic = self.topic_recognizer.recognize_topic(token)
        # if topic == Topic.UNKNOWN:
        #     return Intent.UNKNOWN
        # elif topic == Topic.AMBIGUOUS:
        #     return Intent.AMBIGUOUS
        # elif topic == Topic.CASES:
        #     return self.recognize_cases_intent(token)

    def recognize_value_domain(self, token: Token) -> ValueDomain:
        if self.topic_recognizer.recognize_topic(token) == Topic.UNKNOWN:
            return ValueDomain.UNKNOWN
        elif self.topic_recognizer.recognize_topic(token) == Topic.AMBIGUOUS:
            return ValueDomain.UNKNOWN
        elif self.topic_recognizer.recognize_topic(token) == Topic.CASES:
            return ValueDomain.POSITIVE_CASES
        else:
            people_trigger_words = {self.stemmer.stem(word)
                                    for word in ["human", "people", "person", "individual"]}
        pass


if __name__ == '__main__':
    recognizer = IntentRecognizer()
    recognizer.recognize_intent()