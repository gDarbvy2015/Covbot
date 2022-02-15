from __future__ import annotations
from enum import Enum

import spacy
from lib.nlu.topic import TopicRecognizer, Topic


class Intent(Enum):
    NUMBER_OF_POSITIVE_CASES = 1
    NUMBER_OF_ADMINISTERED_VACCINES = 2
    NUMBER_OF_VACCINATED_PEOPLE = 3
    MAXIMUM_NUMBER_POSITIVE_CASES = 4
    MAXIMUM_NUMBER_DAILY_VACCINATIONS = 5
    COUNTRY_MAXIMUM_NUMBER_POSITIVE_CASES = 6
    DAY_MOST_POSITIVE_CASES = 7
    COUNTRY_HIGHEST_CUMULATIVE_VACCINATIONS = 8
    UNKNOWN = 9
    AMBIGUOUS = 10

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

            if token.lemma_ == "test":
                if "positive" in [child_token.lemma_ for child_token in token.children]:
                    return Intent.NUMBER_OF_POSITIVE_CASES

        return Intent.UNKNOWN


