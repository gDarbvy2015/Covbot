import datetime
import typing
from enum import Enum

import nltk
from nltk import pos_tag
import spacy
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
from dateutil.parser import *
from lib.nlp.nlp_pipeline import NLPPipeline

#from spacy.cli import download as spacy_download
#spacy_download('en')

#nltk.download('punkt')


class Topic(Enum):
    SINGLE_TOPIC = 1
    MULTIPLE_TOPICS = 2
    NOT_SPECIFIED = 3


class Area(Enum):
    ONE_COUNTRY = 1
    MANY_COUNTRIES = 2
    NOT_SPECIFIED = 3
    WORLDWIDE = 4


class TimeFrame(Enum):
    SINGLE_DAY = 1
    TIME_FRAME = 2
    NOT_SPECIFIED = 3


class Intention(Enum):
    NUMBER = 1
    REPORT = 2
    MAXIMUM = 3
    MINIMUM = 4
    DATE = 5
    NOT_SPECIFIED = 6


class IntentRecognizer:
    def __init__(self):
        self.spacy = spacy.load("en_core_web_sm")
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        self.nlp_pipeline = NLPPipeline()

    def get_topic(self, sentence: str) -> (Topic, dict):
        vaccine_triggers = {self.stemmer.stem(word) for word in ["shot", "vaccine", "catch"]}
        case_triggers = {self.stemmer.stem(word) for word in ["case", "infection", "test", "positive"]}

        tokenized_sentence = word_tokenize(sentence)
        pos_tagged_sentence = pos_tag(tokenized_sentence)

        stemmed_tokens = [self.stemmer.stem(word) for word in self._get_stemmed_tokens(pos_tagged_sentence)]

        vaccine_overlaps = vaccine_triggers.intersection(stemmed_tokens)
        case_overlaps = case_triggers.intersection(stemmed_tokens)

        if len(vaccine_overlaps) == 0:
            if len(case_overlaps) == 0:
                return Topic.NOT_SPECIFIED, None
            else:
                return Topic.SINGLE_TOPIC, {"topic": "cases"}
        else:
            if len(case_overlaps) == 0:
                return Topic.SINGLE_TOPIC, {"topic": "vaccinations"}
            else:
                return Topic.MULTIPLE_TOPICS, {"topics": ["cases", "vaccinations"]}

    def get_date(self, sentence: str) -> (TimeFrame, datetime.date):
        annotated_sentence = self.spacy(sentence)
        dates = [ent.text for ent in annotated_sentence.ents if ent.label_ == "DATE"]

        def convert_date(date: str) -> typing.Union[datetime.date, None]:
            try:
                return parse(date).date()
            except ParserError:
                return None

        converted_dates = [actual_date for actual_date in
                           [convert_date(date) for date in dates] if actual_date is not None]

        if len(converted_dates) == 0:
            return TimeFrame.NOT_SPECIFIED, None
        else:
            return TimeFrame.SINGLE_DAY, {"date": converted_dates[0]}

    def get_area(self, sentence: str) -> (TimeFrame, datetime.date):
        annotated_sentence = self.spacy(sentence)
        locations = [self.nlp_pipeline.normalize_country_name(ent.text)
                     for ent in annotated_sentence.ents if ent.label_ == "GPE"]

        if len(locations) == 0:
            return Area.NOT_SPECIFIED, None
        else:
            return Area.ONE_COUNTRY, {"country": locations[0]}

    def _get_stemmed_tokens(self, pos_tagged_tokens: list) -> list:
        stemmed_tokens = []
        for word, tag in pos_tagged_tokens:
            wntag = tag[0].lower()
            wntag = wntag if wntag in ["a", "r", "n", "v"] else None
            if not wntag:
                lemma = word
            else:
                lemma = self.lemmatizer.lemmatize(word, wntag)
            stemmed_tokens.append(lemma)
        return stemmed_tokens


if __name__ == '__main__':
    sent1 = "How many people were infected on 27th of November 2021 in Austria, the USA, the U.S.A"
    sent2 = "How many people caught COVID two days ago in Germany?"

    ir = IntentRecognizer()
    print(ir.get_area(sent1))
    print(ir.get_area(sent2))