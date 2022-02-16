from __future__ import annotations
from enum import Enum

from nltk import PorterStemmer
from spacy.tokens import Token

from lib.nlu.topic import TopicRecognizer, Topic


class Request(Enum):
    SUM = 1
    MAXIMUM = 2
    MINIMUM = 3
    COUNTRY_MAXIMUM = 4
    COUNTRY_MINIMUM = 5
    DAY_MAXIMUM = 6
    DAY_MINIMUM = 7
    UNKNOWN = 8

    @staticmethod
    def from_str(topic_string: str) -> Request:
        if topic_string.lower() == "sum":
            return Request.SUM
        else:
            return Request.UNKNOWN


class Intent(Enum):
    DAILY_POSITIVE_CASES = 1
    DAILY_ADMINISTERED_VACCINES = 2
    DAILY_VACCINATED_PEOPLE = 3
    CUMULATIVE_POSITIVE_CASES = 4
    CUMULATIVE_ADMINISTERED_VACCINES = 5
    CUMULATIVE_VACCINATED_PEOPLE = 6
    UNKNOWN = 7
    AMBIGUOUS = 8

    @staticmethod
    def from_str(topic_string: str) -> Intent:
        if topic_string.lower() == "daily_positive_cases":
            return Intent.DAILY_POSITIVE_CASES
        elif topic_string.lower() == "cumulative_positive_cases":
            return Intent.CUMULATIVE_POSITIVE_CASES
        elif topic_string.lower() == "daily_administered_vaccines":
            return Intent.DAILY_ADMINISTERED_VACCINES
        elif topic_string.lower() == "daily_vaccinated_people":
            return Intent.DAILY_VACCINATED_PEOPLE
        else:
            return Intent.UNKNOWN


class IntentRecognizer:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.topic_recognizer = TopicRecognizer()

    def recognize_intent(self, token: Token) -> Intent:
        topic = self.topic_recognizer.recognize_topic(token)
        if topic == Topic.UNKNOWN:
            return Intent.UNKNOWN
        elif topic == Topic.AMBIGUOUS:
            return Intent.AMBIGUOUS
        elif topic == Topic.CASES:
            return self.recognize_cases_intent(token)

    def recognize_cases_intent(self, token: Token) -> Intent:
        for sub_token in token.subtree:
            ancestors = {parent._.stem.lower() for parent in sub_token.ancestors}

            if sub_token.lower_ == "how":
                if len({"mani"}.union(self.topic_recognizer.get_cases_trigger_words()).intersection(ancestors)) >= 2:
                    return Intent.DAILY_POSITIVE_CASES

            if sub_token._.stem in self.topic_recognizer.get_cases_trigger_words():
                if len({"number", "of"}.intersection(ancestors)) >= 2:
                    return Intent.DAILY_POSITIVE_CASES
        return Intent.UNKNOWN




if __name__ == '__main__':
    recognizer = IntentRecognizer()
    recognizer.recognize_intent()