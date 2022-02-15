from __future__ import annotations
from enum import Enum

import spacy
from lib.nlu.topic import TopicRecognizer, Topic


class Intent(Enum):
    NUMBER_OF_POSITIVE_CASES = 1
    NUMBER_OF_ADMINISTERED_VACCINES = 2
    UNKNOWN = 3
    AMBIGUOUS = 4

    @staticmethod
    def from_str(topic_string: str) -> Intent:
        if topic_string.lower() == "number_of_positive_cases":
            return Intent.NUMBER_OF_POSITIVE_CASES
        elif topic_string.lower() == "number_of_administered_vaccines":
            return Intent.NUMBER_OF_ADMINISTERED_VACCINES
        else:
            return Intent.UNKNOWN


class IntentRecognizer:
    def __init__(self):
        self.topic_recognizer = TopicRecognizer()
        self.spacy = spacy.load("en_core_web_lg")

    def recognize_intent(self, sentence: str) -> Intent:
        topic = self.topic_recognizer.recognize_topic(sentence)
        if topic == Topic.UNKNOWN:
            return Intent.UNKNOWN
        elif topic == Topic.AMBIGUOUS:
            return Intent.AMBIGUOUS
        elif topic == Topic.CASES:
            return self._recognize_cases_intent(sentence)

    def _recognize_cases_intent(self, sentence: str) -> Intent:
        processed_sentence = self.spacy(sentence)

        for token in processed_sentence:
            if token.lower_ == "how":
                if token.head.lower_ == "many":
                    if token.head.head.lemma_ in self.topic_recognizer.get_cases_triggers():
                        return Intent.NUMBER_OF_POSITIVE_CASES

        return Intent.UNKNOWN


