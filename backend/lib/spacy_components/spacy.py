import spacy
from nltk import PorterStemmer

from spacy.tokens import Token, Doc

from lib.nlu.topic import TopicRecognizer

stemmer = PorterStemmer()
topic_recognizer = TopicRecognizer()

Token.set_extension("stem", getter=lambda t: stemmer.stem(t.lemma_))
Doc.set_extension("topic", getter=lambda doc: topic_recognizer.recognize_topic(list(doc.sents)[0].root))


def get_spacy():
    nlp = spacy.load("en_core_web_sm")
    return nlp