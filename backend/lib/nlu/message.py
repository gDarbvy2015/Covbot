from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional, List

from spacy import Language
from spacy.tokens import Span

from lib.nlu.intent import ValueType, CalculationType, ValueDomain, MeasurementType
from lib.nlu.intent.intent import Intent, IntentRecognizer
from lib.nlu.slot.slots import Slots, SlotsFiller
from lib.nlu.topic.topic import Topic, TopicRecognizer
from lib.spacy_components.custom_spacy import get_spacy


class MessageValidationCode(Enum):
    # This means that we should be able to query the user intent and return an answer.
    VALID = 1

    # These valication codes will be returned if there are issues or missing information in the user query, but
    # it is not unexpected that it will be returned.
    NO_LOCATION = 2
    NO_TIMEFRAME = 3
    AMBIGUOUS_TOPIC = 4
    UNKNOWN_TOPIC = 5
    UNKNOWN_MEASUREMENT_TYPE = 6
    UNKNOWN_VALUE_DOMAIN = 7
    UNKNOWN_CALCULATION_TYPE = 8
    UNKNOWN_VALUE_TYPE = 9

    # These are server-side errors and should in theory never occur.
    NO_TOPIC = 10
    NO_INTENT = 11
    NO_SLOTS = 12
    INTENT_MISMATCH = 13
    UNSUPPORTED_ACTION = 14

    @staticmethod
    def get_valid_codes() -> List[MessageValidationCode]:
        return [MessageValidationCode.VALID]

    @staticmethod
    def get_user_query_error_codes() -> List[MessageValidationCode]:
        return [MessageValidationCode.NO_LOCATION, MessageValidationCode.NO_TIMEFRAME, MessageValidationCode.AMBIGUOUS_TOPIC,
                MessageValidationCode.UNKNOWN_TOPIC, MessageValidationCode.UNKNOWN_MEASUREMENT_TYPE, MessageValidationCode.UNKNOWN_VALUE_DOMAIN,
                MessageValidationCode.UNKNOWN_CALCULATION_TYPE, MessageValidationCode.UNKNOWN_VALUE_TYPE]

    @staticmethod
    def get_server_side_error_codes() -> List[MessageValidationCode]:
        return [MessageValidationCode.NO_TOPIC, MessageValidationCode.NO_INTENT,
                MessageValidationCode.NO_SLOTS, MessageValidationCode.INTENT_MISMATCH,
                MessageValidationCode.UNSUPPORTED_ACTION]


@dataclass
class Message:
    topic: Topic
    intent: Intent
    slots: Slots

    @staticmethod
    def validate_message(msg: Message) -> MessageValidationCode:
        single_fields_validation: Optional[MessageValidationCode] = Message._validate_single_fields(msg)
        if single_fields_validation:
            return single_fields_validation

        return Message._validate_intent_with_slots(msg)

    @staticmethod
    def _validate_intent_with_slots(msg: Message) -> MessageValidationCode:
        has_location: bool = msg.slots.location is not None
        has_date: bool = msg.slots.date is not None
        has_both: bool = has_location and has_date

        if msg.intent.value_type == ValueType.NUMBER:
            if msg.intent.calculation_type == CalculationType.RAW_VALUE:
                # We need a location as well as a timeframe to return a daily number.
                if msg.intent.measurement_type == MeasurementType.DAILY:
                    if not has_date:
                        return MessageValidationCode.NO_TIMEFRAME
                    elif not has_location:
                        return MessageValidationCode.NO_LOCATION
                    elif has_both:
                        return MessageValidationCode.VALID
                # We only need a location. If the timeframe is null, we assume that the user is asking for today.
                elif msg.intent.measurement_type == MeasurementType.CUMULATIVE:
                    if not has_location:
                        return MessageValidationCode.NO_LOCATION
                    else:
                        return MessageValidationCode.VALID
            elif msg.intent.calculation_type == CalculationType.SUM:
                # We need a location as well as a timeframe to return a daily number.
                if msg.intent.measurement_type == MeasurementType.DAILY:
                    if not has_date:
                        return MessageValidationCode.NO_TIMEFRAME
                    elif not has_location:
                        return MessageValidationCode.NO_LOCATION
                    elif has_both:
                        return MessageValidationCode.VALID
                # We can't possibly want the sum of a cumulative value.
                elif msg.intent.measurement_type == MeasurementType.CUMULATIVE:
                    return MessageValidationCode.INTENT_MISMATCH
            elif msg.intent.calculation_type in [CalculationType.MAXIMUM, CalculationType.MINIMUM]:
                # We can't possibly want the highest/lowest cumulative value if the value type is a number,
                # if we are looking for the day or the location with the highest/lowest cumulative value.
                if msg.intent.measurement_type == MeasurementType.CUMULATIVE:
                    return MessageValidationCode.INTENT_MISMATCH
                # We need a location as well as a timeframe to return the highest/lowest number.
                elif msg.intent.measurement_type == MeasurementType.DAILY:
                    if not has_date:
                        return MessageValidationCode.NO_TIMEFRAME
                    elif not has_location:
                        return MessageValidationCode.NO_LOCATION
                    elif has_both:
                        return MessageValidationCode.VALID
        elif msg.intent.value_type == ValueType.DAY:
            # We can only want the maximum/minimum when searching for a day.
            if msg.intent.calculation_type in [CalculationType.SUM, CalculationType.RAW_VALUE]:
                return MessageValidationCode.INTENT_MISMATCH
            elif msg.intent.calculation_type in [CalculationType.MAXIMUM, CalculationType.MINIMUM]:
                if msg.intent.measurement_type in [MeasurementType.DAILY, MeasurementType.CUMULATIVE]:
                    # We at least need the location to find out a certain date.
                    if not has_location:
                        return MessageValidationCode.NO_LOCATION
                    else:
                        return MessageValidationCode.VALID
        elif msg.intent.value_type == ValueType.LOCATION:
            # We can only want the maximum/minimum when searching for a location.
            if msg.intent.calculation_type in [CalculationType.SUM, CalculationType.RAW_VALUE]:
                return MessageValidationCode.INTENT_MISMATCH
            elif msg.intent.calculation_type in [CalculationType.MAXIMUM, CalculationType.MINIMUM]:
                # We don't have any mandatory slots in this case.
                if msg.intent.measurement_type in [MeasurementType.DAILY, MeasurementType.CUMULATIVE]:
                    return MessageValidationCode.VALID

        return MessageValidationCode.UNSUPPORTED_ACTION

    @staticmethod
    def _validate_single_fields(msg: Message) -> Optional[MessageValidationCode]:
        if msg.topic is None:
            return MessageValidationCode.NO_TOPIC
        if msg.intent is None:
            return MessageValidationCode.NO_INTENT
        if msg.slots is None:
            return MessageValidationCode.NO_SLOTS

        if msg.topic == Topic.UNKNOWN:
            return MessageValidationCode.UNKNOWN_TOPIC
        if msg.topic == Topic.AMBIGUOUS:
            return MessageValidationCode.AMBIGUOUS_TOPIC

        if msg.intent.value_type == ValueType.UNKNOWN:
            return MessageValidationCode.UNKNOWN_VALUE_TYPE
        if msg.intent.calculation_type == CalculationType.UNKNOWN:
            return MessageValidationCode.UNKNOWN_CALCULATION_TYPE
        if msg.intent.value_domain == ValueDomain.UNKNOWN:
            return MessageValidationCode.UNKNOWN_VALUE_DOMAIN
        if msg.intent.measurement_type == MeasurementType.UNKNOWN:
            return MessageValidationCode.UNKNOWN_MEASUREMENT_TYPE


class MessageBuilder:
    def __init__(self):
        spacy: Language = get_spacy()
        self._topic_recognizer: TopicRecognizer = TopicRecognizer()
        self._intent_recognizer: IntentRecognizer = IntentRecognizer(spacy.vocab)
        self._slots_filler: SlotsFiller = SlotsFiller()

    def create_message(self, span: Span) -> Message:
        topic: Topic = self._topic_recognizer.recognize_topic(span)
        intent: Intent = self._intent_recognizer.recognize_intent(span)
        slots: Slots = self._slots_filler.fill_slots(span)

        return Message(topic, intent, slots)
