from __future__ import annotations
from enum import Enum

from lib.spacy_components.spacy import get_spacy
from nltk import PorterStemmer


class Topic(Enum):
    UNKNOWN = 1
    CASES = 2
    VACCINATIONS = 3
    AMBIGUOUS = 4

    @staticmethod
    def from_str(topic_string: str) -> Topic:
        if topic_string.lower() == "cases":
            return Topic.CASES
        elif topic_string.lower() == "vaccinations":
            return Topic.VACCINATIONS
        elif topic_string.lower() == "ambiguous":
            return Topic.AMBIGUOUS
        else:
            return Topic.UNKNOWN


class TopicRecognizer:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.spacy = get_spacy()

    def recognize_topic(self, sentence: str) -> Topic:
        vaccine_triggers = self.get_vaccine_triggers()
        case_triggers = self.get_cases_triggers()

        processed_sentence = self.spacy(sentence)

        stemmed_tokens = [token._.stem for token in processed_sentence]

        vaccine_overlaps = vaccine_triggers.intersection(stemmed_tokens)
        case_overlaps = case_triggers.intersection(stemmed_tokens)

        if len(vaccine_overlaps) == 0:
            if len(case_overlaps) == 0:
                return Topic.UNKNOWN
            else:
                return Topic.CASES
        else:
            if len(case_overlaps) == 0:
                return Topic.VACCINATIONS
            else:
                return Topic.AMBIGUOUS

    def get_vaccine_triggers(self):
        return {self.stemmer.stem(word) for word in ["shot", "vaccine", "jab"]}

    #TODO: Add better parsing for test and catch
    def get_cases_triggers(self):
        return {self.stemmer.stem(word) for word in ["case", "infection", "test", "positive", "catch"]}
