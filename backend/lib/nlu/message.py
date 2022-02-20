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
        self.topic_recognizer = TopicRecognizer()
        self.intent_recognizer = IntentRecognizer(spacy.vocab)
        self.slots_filler = SlotsFiller()

    def create_message(self, span: Span) -> Message:
        topic = self.topic_recognizer.recognize_topic(span)
        intent = self.intent_recognizer.recognize_intent(span)
        slots = self.slots_filler.fill_slots(span)

        return Message(topic, intent, slots)