import spacy
from nltk import PorterStemmer
from spacy.lang.en import Language

from spacy.tokens import Token

nlp: Language = spacy.load("en_core_web_lg")
stemmer: PorterStemmer = PorterStemmer()

Token.set_extension("stem", getter=lambda t: stemmer.stem(t.lemma_))


def get_spacy() -> Language:
    return nlp
