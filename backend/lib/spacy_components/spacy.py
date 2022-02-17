import spacy
from nltk import PorterStemmer

from spacy.tokens import Token, Doc

from lib.nlu.intent import IntentRecognizer
from lib.nlu.location import LocationRecognizer
from lib.nlu.topic import TopicRecognizer

stemmer = PorterStemmer()
topic_recognizer = TopicRecognizer()
intent_recognizer = IntentRecognizer()
location_recognizer = LocationRecognizer()

Token.set_extension("stem", getter=lambda t: stemmer.stem(t.lemma_))
Doc.set_extension("topic", getter=lambda doc: topic_recognizer.recognize_topic(list(doc.sents)[0].root))
Doc.set_extension("intent", getter=lambda doc: intent_recognizer.recognize_intent(list(doc.sents)[0].root))
Doc.set_extension("location", getter=lambda doc: location_recognizer.recognize_location(doc))

nlp = spacy.load("en_core_web_lg")


def get_spacy():
    return nlp