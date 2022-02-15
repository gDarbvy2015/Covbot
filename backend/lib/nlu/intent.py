from __future__ import annotations
from enum import Enum

from lib.spacy_components.spacy import get_spacy
from nltk import PorterStemmer
from spacy.tokens import Token

from lib.nlu.topic import TopicRecognizer, Topic


class Request(Enum):
    SUM = 1
    MAXIMUM = 2
    MINIMUM = 3
    COUNTRY_MAXIMUM = 4
    COUNTRY_MINIMUM = 5
    DAY_MAXIMUM = 6
    DAY_MINIMUM = 7
    UNKNOWN = 8

    @staticmethod
    def from_str(topic_string: str) -> Request:
        if topic_string.lower() == "sum":
            return Request.SUM
        else:
            return Request.UNKNOWN


class Intent(Enum):
    DAILY_POSITIVE_CASES = 1
    DAILY_ADMINISTERED_VACCINES = 2
    DAILY_VACCINATED_PEOPLE = 3
    CUMULATIVE_POSITIVE_CASES = 4
    CUMULATIVE_ADMINISTERED_VACCINES = 5
    CUMULATIVE_VACCINATED_PEOPLE = 6
    UNKNOWN = 7
    AMBIGUOUS = 8

    @staticmethod
    def from_str(topic_string: str) -> Intent:
        if topic_string.lower() == "daily_positive_cases":
            return Intent.DAILY_POSITIVE_CASES
        elif topic_string.lower() == "daily_administered_vaccines":
            return Intent.DAILY_ADMINISTERED_VACCINES
        elif topic_string.lower() == "daily_vaccinated_people":
            return Intent.DAILY_VACCINATED_PEOPLE
        else:
            return Intent.UNKNOWN


class IntentRecognizer:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.topic_recognizer = TopicRecognizer()
        self.spacy = get_spacy()

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
                    if token.head.head._.stem in self.topic_recognizer.get_cases_trigger_words():
                        return Intent.DAILY_POSITIVE_CASES

            if token.lemma_ == "test":
                adjectives = {self.stemmer.stem(word) for word in ["positive", "confirmed"]}
                if len(adjectives.intersection({child_token._.stem for child_token in token.children})) > 0:
                    return Intent.DAILY_POSITIVE_CASES

            if token.lemma_ in ["number", "amount"]:
                if self._check_for_trigger_word_recursively(token):
                    return Intent.DAILY_POSITIVE_CASES

        return Intent.UNKNOWN

    def _check_for_trigger_word_recursively(self, token: Token) -> bool:
        stemmed_token = token._.stem

        if stemmed_token in self.topic_recognizer.get_cases_trigger_words():
            return True

        for child_token in token.children:
            stemmed_child_token = child_token._.stem
            if stemmed_token != stemmed_child_token:
                if self._check_for_trigger_word_recursively(child_token):
                    return True
        return False



if __name__ == '__main__':
    recognizer = IntentRecognizer()
    recognizer.recognize_intent("")