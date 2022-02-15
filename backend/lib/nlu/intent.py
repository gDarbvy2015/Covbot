from __future__ import annotations
from enum import Enum

import spacy
from nltk import PorterStemmer

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
        elif topic_string.lower() == "daily_administered_vaccines":
            return Intent.DAILY_ADMINISTERED_VACCINES
        elif topic_string.lower() == "daily_vaccinated_people":
            return Intent.DAILY_VACCINATED_PEOPLE
        else:
            return Intent.UNKNOWN


class IntentRecognizer:
    def __init__(self):
        self.topic_recognizer = TopicRecognizer()
        self.stemmer = PorterStemmer()
        self.spacy = spacy.load("en_core_web_lg")

    def recognize_intent(self, sentence: str) -> Intent:
        topic = self.topic_recognizer.recognize_topic(sentence)
        if topic == Topic.UNKNOWN:
            return Intent.UNKNOWN
        elif topic == Topic.AMBIGUOUS:
            return Intent.AMBIGUOUS
        elif topic == Topic.CASES:
            return self._recognize_cases_intent(sentence)

    def _recognize_cases_intent(self, sentence: str) -> Intent:
        processed_sentence = self.spacy(sentence)

        for token in processed_sentence:
            if token.lower_ == "how":
                if token.head.lower_ == "many":
                    if self.stemmer.stem(token.head.head.lemma_) in self.topic_recognizer.get_cases_triggers():
                        return Intent.DAILY_POSITIVE_CASES

            if token.lemma_ == "test":
                adjectives = {self.stemmer.stem(word) for word in ["positive", "confirmed"]}
                if len(adjectives.intersection({self.stemmer.stem(child_token.lemma_) for child_token in token.children})) > 0:
                    return Intent.DAILY_POSITIVE_CASES

        return Intent.UNKNOWN


if __name__ == '__main__':
    recognizer = IntentRecognizer()
    recognizer.recognize_intent("")