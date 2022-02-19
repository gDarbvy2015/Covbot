from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional

import spacy
from nltk import PorterStemmer
from spacy.tokens import Token
from spacy.tokens.span import Span

from lib.nlu.patterns import human_pattern, vaccine_trigger_pattern, \
    how_many_pattern, what_day_pattern, when_pattern, where_pattern, what_country_pattern, what_is_country_pattern

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
    def __init__(self, vocab=None, pipeline=None):
        if pipeline is None:
            pipeline = [ValueDomain]

        self.stemmer = PorterStemmer()
        self.pipeline = pipeline
        self.topic_recognizer = TopicRecognizer()

        if MeasurementType in pipeline:
            self.date_recognizer = DateRecognizer()

        self.vocab = vocab

    def recognize_intent(self, span: Span) -> Optional[Intent]:

        value_domain = self.recognize_value_domain(span) if ValueDomain in self.pipeline else ValueDomain.UNKNOWN
        measurement_type = MeasurementType.UNKNOWN
        value_type = ValueType.UNKNOWN
        calculation_type = CalculationType.UNKNOWN

        return Intent(calculation_type, value_type, value_domain, measurement_type)

    def recognize_value_domain(self, span: Span) -> ValueDomain:
        topic = self.topic_recognizer.recognize_topic(span)
        if topic == Topic.CASES:
            return ValueDomain.POSITIVE_CASES
        elif topic == Topic.VACCINATIONS:

            matcher = DependencyMatcher(self.vocab)
            matcher.add("human", [human_pattern])
            matcher.add("vaccine", [vaccine_trigger_pattern])
            result = matcher(span.as_doc())

            matched_patterns = {pattern_id for pattern_id, token_pos in result}

            if len(matched_patterns) > 1:
                return ValueDomain.VACCINATED_PEOPLE
            else:
                return ValueDomain.ADMINISTERED_VACCINES

        else:
            return ValueDomain.UNKNOWN

    def recognize_measurement_type(self, token: Token) -> MeasurementType:
        timeframe = self.date_recognizer.recognize_date(str(token.sent))
        topic = self.topic_recognizer.recognize_topic(token)

        if topic in [Topic.CASES, Topic.VACCINATIONS]:
            if timeframe is not None:
                return MeasurementType.DAILY
            else:
                return MeasurementType.CUMULATIVE
        else:
            return MeasurementType.UNKNOWN

    def recognize_value_type(self, span: Span) -> ValueType:
        topic = self.topic_recognizer.recognize_topic(span)
        if topic in [Topic.CASES, Topic.VACCINATIONS]:
            if self._has_valid_when_pattern(span):
                return ValueType.DAY
            if self._has_valid_where_pattern(span):
                return ValueType.LOCATION
            if self._has_valid_how_many_pattern(span):
                return ValueType.NUMBER
            else:
                return ValueType.UNKNOWN
        else:
            return ValueType.UNKNOWN

    def _has_valid_when_pattern(self, span: Span) -> bool:
        matcher = DependencyMatcher(self.vocab)

        matcher.add("when", [what_day_pattern, when_pattern])

        result = matcher(span)
        return len(result) > 0

    def _has_valid_how_many_pattern(self, span: Span) -> bool:
        matcher = DependencyMatcher(self.vocab)

        matcher.add("how_many", [how_many_pattern])

        result = matcher(span)
        return len(result) > 0

    def _has_valid_where_pattern(self, span: Span) -> bool:
        matcher = DependencyMatcher(self.vocab)

        matcher.add("where", [where_pattern, what_country_pattern, what_is_country_pattern])

        result = matcher(span)
        return len(result) > 0


if __name__ == '__main__':
    pass