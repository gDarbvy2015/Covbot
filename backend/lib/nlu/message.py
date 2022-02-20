from dataclasses import dataclass

from spacy.tokens import Span

from lib.nlu.intent.intent import Intent, IntentRecognizer
from lib.nlu.slot.slots import Slots, SlotsFiller
from lib.nlu.topic.topic import Topic, TopicRecognizer
from lib.spacy_components.spacy import get_spacy


@dataclass
class Message:
    topic: Topic
    intent: Intent
    slots: Slots


class MessageBuilder:
    def __init__(self):
        spacy = get_spacy()
        self._topic_recognizer = TopicRecognizer()
        self._intent_recognizer = IntentRecognizer(spacy._vocab)
        self._slots_filler = SlotsFiller()

    def create_message(self, span: Span) -> Message:
        topic = self._topic_recognizer.recognize_topic(span)
        intent = self._intent_recognizer.recognize_intent(span)
        slots = self._slots_filler.fill_slots(span)

        return Message(topic, intent, slots)