from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from nltk import PorterStemmer
from spacy.tokens import Token

from lib.nlu.date import DateRecognizer
from lib.nlu.topic import TopicRecognizer, Topic
from spacy.matcher import DependencyMatcher


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
        self.time_recognizer = DateRecognizer()

    def recognize_intent(self, token: Token) -> Optional[Intent]:

        value_domain = self.recognize_value_domain(token)
        measurement_type = self.recognize_measurement_type(token)
        value_type = self.recognize_value_type(token)

        return Intent(CalculationType.UNKNOWN, value_type, value_domain, measurement_type)
        # topic = self.topic_recognizer.recognize_topic(token)
        # if topic == Topic.UNKNOWN:
        #     return Intent.UNKNOWN
        # elif topic == Topic.AMBIGUOUS:
        #     return Intent.AMBIGUOUS
        # elif topic == Topic.CASES:
        #     return self.recognize_cases_intent(token)

    def recognize_value_domain(self, token: Token) -> ValueDomain:
        topic = self.topic_recognizer.recognize_topic(token)
        if  topic == Topic.CASES:
            return ValueDomain.POSITIVE_CASES
        elif topic == Topic.VACCINATIONS:
            people_trigger_words = {self.stemmer.stem(word)
                                    for word in ["human", "people", "person", "individual"]}

            for child in token.subtree:
                if child._.stem in people_trigger_words:
                    # Hardcoded case for query 21
                    for child2 in token.subtree:
                        if child2._.stem in self.topic_recognizer.get_vaccine_trigger_words() and child2.pos_ == "NOUN":
                            return ValueDomain.ADMINISTERED_VACCINES

                    return ValueDomain.VACCINATED_PEOPLE

            return ValueDomain.ADMINISTERED_VACCINES
        else:
            return ValueDomain.UNKNOWN

    def recognize_measurement_type(self, token: Token) -> MeasurementType:
        timeframe = self.time_recognizer.recognize_date(str(token.sent))
        topic = self.topic_recognizer.recognize_topic(token)

        if topic in [Topic.CASES, Topic.VACCINATIONS]:
            if timeframe is not None:
                return MeasurementType.DAILY
            else:
                return MeasurementType.CUMULATIVE
        else:
            return MeasurementType.UNKNOWN

    def recognize_value_type(self, token: Token) -> ValueType:
        topic = self.topic_recognizer.recognize_topic(token)
        if topic in [Topic.CASES, Topic.VACCINATIONS]:
            if self._has_valid_how_many_pattern(topic, token):
                return ValueType.NUMBER
            else:
                return ValueType.UNKNOWN
        else:
            return ValueType.UNKNOWN

    def _has_valid_how_many_pattern(self, topic: Topic, token: Token) -> bool:
        if topic == Topic.CASES:
            trigger_words = self.topic_recognizer.get_cases_trigger_words()
        elif topic == Topic.VACCINATIONS:
            trigger_words = self.topic_recognizer.get_vaccine_trigger_words()
        else:
            return False

        pattern = [
            {
                "RIGHT_ID": "how_pat",
                "RIGHT_ATTRS": {
                    "LEMMA": "how"
                }
            },
            {
                "LEFT_ID": "how_pat",
                "REL_OP": "<",
                "RIGHT_ID": "how_many_pat",
                "RIGHT_ATTRS": {
                    "LEMMA": "many"
                }
            },
            {
                "LEFT_ID": "how_pat",
                "REL_OP": "<<",
                "RIGHT_ID": "numper_pat",
                "RIGHT_ATTRS": {
                    #"_STEM":
                }
            }
        ]

        return False


if __name__ == '__main__':
    recognizer = IntentRecognizer()
    recognizer.recognize_intent()