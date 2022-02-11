from enum import Enum

import nltk
from nltk import pos_tag
import spacy
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize


class Topic(Enum):
    VACCINATION = 1
    POSITIVE_CASE = 2
    UNSURE = 3
    UNKNOWN = 4


class Area(Enum):
    COUNTRY = 1
    CONTINENT = 2
    UNKNOWN = 3
    WORLDWIDE = 4


class Intention(Enum):
    NUMBER = 1
    REPORT = 2
    MAXIMUM = 3
    MINIMUM = 4
    DATE = 5
    UNKNOWN = 6


class IntentRecognizer:
    def __init__(self):
        self.spacy = spacy.load("en_core_web_sm")
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()

    def get_topic(self, sentence: str) -> Topic:
        vaccine_triggers = {self.stemmer.stem(word) for word in ["shot", "vaccine", "catch"]}
        case_triggers = {self.stemmer.stem(word) for word in ["case", "infection", "test", "positive"]}

        tokenized_sentence = word_tokenize(sentence)
        pos_tagged_sentence = pos_tag(tokenized_sentence)

        stemmed_tokens = [self.stemmer.stem(word) for word in self._get_stemmed_tokens(pos_tagged_sentence)]

        vaccine_overlaps = vaccine_triggers.intersection(stemmed_tokens)
        case_overlaps = case_triggers.intersection(stemmed_tokens)

        if len(vaccine_overlaps) == 0:
            if len(case_overlaps) == 0:
                return Topic.UNKNOWN
            else:
                return Topic.POSITIVE_CASE
        else:
            if len(case_overlaps) == 0:
                return Topic.VACCINATION
            else:
                return Topic.UNSURE

    def _get_stemmed_tokens(self, pos_tagged_tokens: list) -> list:
        stemmed_tokens = []
        for word, tag in pos_tagged_tokens:
            wntag = tag[0].lower()
            wntag = wntag if wntag in ['a', 'r', 'n', 'v'] else None
            if not wntag:
                lemma = word
            else:
                lemma = self.lemmatizer.lemmatize(word, wntag)
            stemmed_tokens.append(lemma)
        return stemmed_tokens


if __name__ == '__main__':
    sent1 = "How many people were infected on the 27th of November 2021 in Austria"
    sent2 = "How many people caught COVID two days ago in Germany?"

    ir = IntentRecognizer()
    print(ir.get_topic(sent1))
    print(ir.get_topic(sent2))