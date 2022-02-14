from __future__ import annotations
from enum import Enum

from nltk import PorterStemmer, WordNetLemmatizer, word_tokenize, pos_tag


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
        self.lemmatizer = WordNetLemmatizer()

    def recognize_topic(self, sentence: str) -> Topic:
        vaccine_triggers = self.get_vaccine_triggers()
        case_triggers = self.get_cases_triggers()

        tokenized_sentence = word_tokenize(sentence)
        pos_tagged_sentence = pos_tag(tokenized_sentence)

        stemmed_tokens = [self.stemmer.stem(word) for word in self._get_lemmatized_tokens(pos_tagged_sentence)]

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

    def get_cases_triggers(self):
        return {self.stemmer.stem(word) for word in ["case", "infection", "test", "positive", "catch"]}

    def _get_lemmatized_tokens(self, pos_tagged_tokens: list) -> list:
        lemmatized_tokens = list()
        for word, tag in pos_tagged_tokens:
            # We need to include pos tags so that verbs are lemmatized correctly (for example 'caught' -> 'catch')
            wntag = tag[0].lower()
            wntag = wntag if wntag in ["a", "r", "n", "v"] else None
            if not wntag:
                lemma = word
            else:
                lemma = self.lemmatizer.lemmatize(word, wntag)
            lemmatized_tokens.append(lemma)
        return lemmatized_tokens
