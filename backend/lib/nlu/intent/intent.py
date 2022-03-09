from __future__ import annotations

from dataclasses import dataclass

from nltk import PorterStemmer
from spacy.matcher import DependencyMatcher
from spacy.tokens.span import Span

from lib.nlu.intent.calculation_type import CalculationType
from lib.nlu.intent.measurement_type import MeasurementType
from lib.nlu.intent.value_domain import ValueDomain
from lib.nlu.intent.value_type import ValueType
from lib.nlu.patterns import Pattern
from lib.nlu.slot.date import DateRecognizer, Date
from lib.nlu.topic.topic import TopicRecognizer, Topic
from lib.spacy_components.custom_spacy import get_spacy, CustomSpacy


@dataclass
class Intent:
    """Class representing the intent of a query.
    For more information on each of the attributes, check the documentation of the respective classes.
    """
    calculation_type: CalculationType
    value_type: ValueType
    value_domain: ValueDomain
    measurement_type: MeasurementType


class IntentRecognizer:
    """Class providing helper methods to recognize the intent of a query."""
    def __init__(self):
        self._stemmer: PorterStemmer = PorterStemmer()
        self._topic_recognizer: TopicRecognizer = TopicRecognizer()
        self._date_recognizer: DateRecognizer = DateRecognizer()

    def recognize_intent(self, span: Span) -> Intent:
        """Recognize the intent of a span."""
        value_domain: ValueDomain = self.recognize_value_domain(span)
        measurement_type: MeasurementType = self.recognize_measurement_type(span)
        value_type: ValueType = self.recognize_value_type(span)
        calculation_type: CalculationType = self.recognize_calculation_type(span)

        return Intent(calculation_type, value_type, value_domain, measurement_type)

    def recognize_calculation_type(self, span: Span):
        """Recognize the calculation type of a span."""
        date: Date = self._date_recognizer.recognize_date(span)
        value_type: ValueType = self.recognize_value_type(span)

        # e.g. "What is the highest number of cases recorded in Austria?".
        if Pattern.has_valid_pattern(span, [Pattern.maximum_number_pattern, Pattern.most_trigger_word_pattern]):
            return CalculationType.MAXIMUM
        # e.g. "What is the smallest number of cases recorded in Austria this week?".
        if Pattern.has_valid_pattern(span, [Pattern.minimum_number_pattern, Pattern.least_trigger_word_pattern]):
            return CalculationType.MINIMUM

        # If we were asking about a day or a location, it either has to be maximum or minimum, so by now
        # it must be a number.
        if value_type != ValueType.NUMBER:
            return CalculationType.UNKNOWN

        # If we don't have a time frame, the user either forgot to supply it or the user is asking for a cumulative
        # value (e.g. "How many cases have there been in Austria so far?"). So in this case, we return the raw value.
        if date is None:
            return CalculationType.RAW_VALUE
        # If the supplied date by the user is a single day, we also just need the raw_value from that date
        # (e.g. "How many cases have there been in Austria on the 25th of December?")
        if date.type == "DAY":
            return CalculationType.RAW_VALUE
        else:
            return CalculationType.SUM

    def recognize_value_domain(self, span: Span) -> ValueDomain:
        """Recognize the value domain of a span."""
        topic: Topic = self._topic_recognizer.recognize_topic(span)
        if topic == Topic.CASES:
            return ValueDomain.POSITIVE_CASES
        # Distinguish between "how many vaccines have been administered" and "how many people have been vaccinated".
        elif topic == Topic.VACCINATIONS:

            matcher: DependencyMatcher = DependencyMatcher(CustomSpacy.get_spacy().vocab)
            matcher.add("human", [Pattern.human_pattern])
            matcher.add("vaccine", [Pattern.vaccine_trigger_pattern])
            result: list = matcher(span.as_doc())

            matched_patterns: set = {pattern_id for pattern_id, token_pos in result}

            if len(matched_patterns) > 1:
                return ValueDomain.VACCINATED_PEOPLE
            else:
                return ValueDomain.ADMINISTERED_VACCINES
        else:
            return ValueDomain.UNKNOWN

    def recognize_measurement_type(self, span: Span) -> MeasurementType:
        """Recognize the measurement type of a span."""
        date = self._date_recognizer.recognize_date(span)
        value_type = self.recognize_value_type(span)
        calculation_type = self.recognize_calculation_type(span)

        if value_type == ValueType.LOCATION:
            # If there is no date, we are surely asking for the cumulative value, since we are comparing
            # different countries.
            # e.g. "Which country has the the most vaccinated people?"
            if date is None:
                return MeasurementType.CUMULATIVE
            # Otherwise we want the daily value.
            # e.g. "Which country had the most administered vaccines yesterday?"
            # This is technically not always the case, because we could for example ask
            # "Which country had the most administered vaccines in total yesterday?", which would
            # require the cumulative value. But we are going to disregard this case for the sake of simplicity.
            else:
                return MeasurementType.DAILY
        elif value_type == ValueType.DAY:
            # If we are asking for a certain day, we default to the daily value.
            # e.g. "On which day were most cases recorded in Austria?"
            # As above, this also is an simplification, as we could in theory ask something like
            # "On which day did Austria have the highest number of cases in total", but this question doesn't
            # really make sense since it's always going to be the closest date to today.
            return MeasurementType.DAILY
        elif value_type == ValueType.NUMBER:
            # In this case, we must be asking for the highest/lowest number in a certain location in some time
            # period, so we can default to daily.
            # e.g. "What was the highest number of cases recorded in Austria last week?"
            if calculation_type in [CalculationType.MAXIMUM, CalculationType.MINIMUM]:
                return MeasurementType.DAILY
            elif calculation_type == CalculationType.RAW_VALUE:
                # If we don't have a date and are looking for the raw value, we give the cumulative value of
                # today by default.
                # e.g. "What is the number of cases in Austria?"
                if date is None:
                    return MeasurementType.CUMULATIVE
                # Otherwise, we are either asking for a single day or the sum over a certain time period,
                # so we return the daily number.
                # e.g. "How many new cases have been reported in Austria last week?"
                else:
                    return MeasurementType.DAILY
            # For a sum, we never use the cumulative value, since the cumulative value already is a by itself.
            elif calculation_type == CalculationType.SUM:
                return MeasurementType.DAILY

        return MeasurementType.UNKNOWN

    def recognize_value_type(self, span: Span) -> ValueType:
        """Recognize the value type of a span."""
        # Use each of the pre-defined patterns to understand what type of value the user is asking from us.
        # e.g. "When did Austria have the most Corona cases?"
        if Pattern.has_valid_pattern(span, [Pattern.what_day_pattern, Pattern.when_pattern]):
            return ValueType.DAY
        # e.g. "Where have most Corona cases been reported?"
        elif Pattern.has_valid_pattern(span, [Pattern.where_pattern, Pattern.what_country_pattern,
                                            Pattern.what_is_country_pattern]):
            return ValueType.LOCATION
        # e.g. "What is the number of new Corona cases in Austria today?"
        elif Pattern.has_valid_pattern(span, [Pattern.how_many_pattern, Pattern.number_of_pattern]):
            return ValueType.NUMBER
        # If we don't have any other clues but there are trigger words, we assume that we are asking for the number
        # e.g. "vaccinations worldwide today" (query with id 20)
        elif Pattern.has_valid_pattern(span, [Pattern.case_trigger_pattern, Pattern.vaccine_trigger_pattern]):
            return ValueType.NUMBER

        return ValueType.UNKNOWN