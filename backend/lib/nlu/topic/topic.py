from __future__ import annotations
from enum import Enum
from typing import Optional

from spacy.tokens import Token, Span
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
        self._stemmer = PorterStemmer()

    def recognize_topic(self, span: Span) -> Topic:
        is_topic_vaccine = self.is_topic_vaccine(span)
        is_topic_cases = self.is_topic_cases(span)

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

    def is_topic_vaccine(self, span: Span) -> bool:
        vaccine_triggers = self.get_vaccine_trigger_words()
        related_tokens = [token._.stem for token in span]
        vaccine_overlaps = vaccine_triggers.intersection(related_tokens)

        is_right_topic = len(vaccine_overlaps) >= 1
        return is_right_topic

    def is_topic_cases(self, span: Span) -> bool:
        case_triggers = self.get_cases_trigger_words()
        related_tokens = [token._.stem for token in span]
        case_overlaps = case_triggers.intersection(related_tokens)

        is_right_topic = len(case_overlaps) >= 1
        return is_right_topic

    def is_vaccine_trigger_word(self, token: Token) -> bool:
        return token._.stem in self.get_vaccine_trigger_words()

    def is_cases_trigger_word(self, token: Token) -> bool:
        return token._.stem in self.get_cases_trigger_words()

    def get_vaccine_trigger_words(self):
        return {self._stemmer.stem(word) for word in ["shot", "vaccine", "jab", "inoculation", "immunization",
                                                     "administer"]}

    def get_cases_trigger_words(self):
        return {self._stemmer.stem(word) for word in ["case", "infection", "test", "positive", "negative"]}
