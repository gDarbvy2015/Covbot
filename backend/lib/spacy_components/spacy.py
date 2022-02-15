import spacy
from nltk import PorterStemmer

from spacy.tokens import Token

stemmer = PorterStemmer()
Token.set_extension("stem", getter=lambda t: stemmer.stem(t.lemma_))


def get_spacy():
    nlp = spacy.load("en_core_web_sm")
    return nlp