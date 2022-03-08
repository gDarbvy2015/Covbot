from __future__ import annotations

from enum import Enum
from typing import Optional, List

from nltk import PorterStemmer
from spacy.tokens import Token, Span

from lib.nlu.patterns import Pattern


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
        self._stemmer: PorterStemmer = PorterStemmer()

    def recognize_topic(self, span: Span) -> Topic:
        is_topic_vaccine: bool = self.is_topic_vaccine(span)
        is_topic_cases: bool = self.is_topic_cases(span)

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
        return Pattern.has_valid_pattern(span, [Pattern.vaccine_trigger_pattern])

    def is_topic_cases(self, span: Span) -> bool:
        # Special case: "How many people got COVID" vs. "How many people got the COVID vaccine"
        if Pattern.has_valid_pattern(span, [Pattern.covid_pattern]) and not Pattern.has_valid_pattern(
                span, [Pattern.covid_vaccine_pattern]):
            return True
        return Pattern.has_valid_pattern(span, [Pattern.case_trigger_pattern])
