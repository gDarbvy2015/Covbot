from dataclasses import dataclass

from spacy import Language
from spacy.tokens import Span

from lib.nlu.intent.intent import Intent, IntentRecognizer
from lib.nlu.slot.slots import Slots, SlotsFiller
from lib.nlu.topic.topic import Topic, TopicRecognizer
from lib.spacy_components.custom_spacy import get_spacy


@dataclass
class Message:
    topic: Topic
    intent: Intent
    slots: Slots


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
