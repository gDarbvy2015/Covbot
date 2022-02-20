from __future__ import annotations

from dataclasses import dataclass

from nltk import PorterStemmer
from spacy.tokens.span import Span

from lib.nlu.intent.calculation_type import CalculationType
from lib.nlu.intent.measurement_type import MeasurementType
from lib.nlu.intent.value_domain import ValueDomain
from lib.nlu.intent.value_type import ValueType
from lib.nlu.patterns import Pattern

from lib.nlu.slot.date import DateRecognizer
from lib.nlu.topic.topic import TopicRecognizer, Topic
from spacy.matcher import DependencyMatcher


@dataclass
class Intent:
    calculation_type: CalculationType
    value_type: ValueType
    value_domain: ValueDomain
    measurement_type: MeasurementType


class IntentRecognizer:
    def __init__(self, vocab):
        self._stemmer = PorterStemmer()
        self._topic_recognizer = TopicRecognizer()
        self._date_recognizer = DateRecognizer()
        self._vocab = vocab

    def recognize_intent(self, span: Span) -> Intent:
        value_domain = self.recognize_value_domain(span)
        measurement_type = self.recognize_measurement_type(span)
        value_type = self.recognize_value_type(span)
        calculation_type = self.recognize_calculation_type(span)

        return Intent(calculation_type, value_type, value_domain, measurement_type)

    def recognize_calculation_type(self, span: Span):
        value_type = self.recognize_value_type(span)
        timeframe = self._date_recognizer.recognize_date(span)

        if value_type == ValueType.UNKNOWN:
            return CalculationType.UNKNOWN
        if self._has_valid_pattern(span, [Pattern.maximum_number_pattern, Pattern.most_trigger_word_pattern]):
            return CalculationType.MAXIMUM
        if self._has_valid_pattern(span, [Pattern.minimum_number_pattern, Pattern.least_trigger_word_pattern]):
            return CalculationType.MINIMUM
        # If we don't have any time indication, we automatically pick the cumulative value of the nearest date,
        # so the raw value
        if timeframe is None:
            return CalculationType.RAW_VALUE
        if timeframe.value["time"] == "DAY":
            return CalculationType.RAW_VALUE
        else:
            return CalculationType.SUM

    def recognize_value_domain(self, span: Span) -> ValueDomain:
        topic = self._topic_recognizer.recognize_topic(span)
        if topic == Topic.CASES:
            return ValueDomain.POSITIVE_CASES
        elif topic == Topic.VACCINATIONS:

            matcher = DependencyMatcher(self._vocab)
            matcher.add("human", [Pattern.human_pattern])
            matcher.add("vaccine", [Pattern.vaccine_trigger_pattern])
            result = matcher(span.as_doc())

            matched_patterns = {pattern_id for pattern_id, token_pos in result}

            if len(matched_patterns) > 1:
                return ValueDomain.VACCINATED_PEOPLE
            else:
                return ValueDomain.ADMINISTERED_VACCINES

        else:
            return ValueDomain.UNKNOWN

    def recognize_measurement_type(self, span: Span) -> MeasurementType:
        timeframe = self._date_recognizer.recognize_date(span)
        topic = self._topic_recognizer.recognize_topic(span)
        value_type = self.recognize_value_type(span)
        calculation_type = self.recognize_calculation_type(span)

        if topic in [Topic.CASES, Topic.VACCINATIONS]:
            if timeframe is None:
                if calculation_type in [CalculationType.SUM]:
                    return MeasurementType.DAILY
                else:
                    if value_type in [ValueType.NUMBER, ValueType.DAY] and calculation_type not in [CalculationType.RAW_VALUE]:
                        return MeasurementType.DAILY
                    else:
                        return MeasurementType.CUMULATIVE
            else:
                if value_type == ValueType.LOCATION:
                    return MeasurementType.CUMULATIVE
                else:
                    return MeasurementType.DAILY
        else:
            return MeasurementType.UNKNOWN

    def recognize_value_type(self, span: Span) -> ValueType:
        topic = self._topic_recognizer.recognize_topic(span)
        if topic in [Topic.CASES, Topic.VACCINATIONS]:
            if self._has_valid_pattern(span, [Pattern.what_day_pattern, Pattern.when_pattern]):
                return ValueType.DAY
            elif self._has_valid_pattern(span, [Pattern.where_pattern, Pattern.what_country_pattern, Pattern.what_is_country_pattern]):
                return ValueType.LOCATION
            elif self._has_valid_pattern(span, [Pattern.how_many_pattern]):
                return ValueType.NUMBER
            elif self._has_valid_pattern(span, [Pattern.number_of_pattern]):
                return ValueType.NUMBER
            # If we don't have any other clues but there are trigger words, we assume that we are asking for the number
            # (for example query 20, 23, 24)
            elif self._has_valid_pattern(span, [Pattern.case_trigger_pattern, Pattern.vaccine_trigger_pattern]):
                return ValueType.NUMBER
            else:
                return ValueType.UNKNOWN
        else:
            return ValueType.UNKNOWN

    def _has_valid_pattern(self, span: Span, pattern: list) -> bool:
        matcher = DependencyMatcher(self._vocab)

        matcher.add("pattern", pattern)

        result = matcher(span)
        return len(result) > 0


if __name__ == '__main__':
    pass