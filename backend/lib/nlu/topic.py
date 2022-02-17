from __future__ import annotations
from enum import Enum
from typing import Optional

from spacy.tokens import Token
from nltk import PorterStemmer


class Topic(Enum):
    CASES = 1
    VACCINATIONS = 2
    AMBIGUOUS = 3
    UNKNOWN = 4

    @staticmethod
    def from_str(topic: str) -> Optional[Topic]:
        try:
            return Topic[topic.upper()]
        except KeyError:
            return Topic["UNKNOWN"]


class TopicRecognizer:
    def __init__(self):
        self.stemmer = PorterStemmer()

    def recognize_topic(self, token: Token) -> Topic:
        is_topic_vaccine = self.is_topic_vaccine(token)
        is_topic_cases = self.is_topic_cases(token)

        if is_topic_vaccine:
            if is_topic_cases:
                return Topic.AMBIGUOUS
            else:
                return Topic.VACCINATIONS
        else:
            if is_topic_cases:
                return Topic.CASES
            else:
                return Topic.UNKNOWN

    def is_topic_vaccine(self, token: Token) -> bool:
        vaccine_triggers = self.get_vaccine_trigger_words()
        related_tokens = [iter_token._.stem for iter_token in list(token.subtree)]
        vaccine_overlaps = vaccine_triggers.intersection(related_tokens)

        is_right_topic = len(vaccine_overlaps) >= 1
        return is_right_topic

    def is_topic_cases(self, token: Token) -> bool:
        case_triggers = self.get_cases_trigger_words()
        related_tokens = [iter_token._.stem for iter_token in list(token.subtree)]
        case_overlaps = case_triggers.intersection(related_tokens)

        is_right_topic = len(case_overlaps) >= 1
        return is_right_topic

    def get_vaccine_trigger_words(self):
        return {self.stemmer.stem(word) for word in ["shot", "vaccine", "jab", "inoculation", "immunization",
                                                     "administer"]}

    def get_cases_trigger_words(self):
        return {self.stemmer.stem(word) for word in ["case", "infection", "test", "positive", "negative"]}
