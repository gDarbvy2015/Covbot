from typing import Optional

import spacy
from nltk import PorterStemmer
from spacy.lang.en import Language

from spacy.tokens import Token

stemmer: PorterStemmer = PorterStemmer()

Token.set_extension("stem", getter=lambda t: stemmer.stem(t.lemma_))


class CustomSpacy:
    nlp: Optional[Language] = None

    @staticmethod
    def get_spacy() -> Language:
        if CustomSpacy.nlp is None:
            CustomSpacy.nlp = spacy.load("en_core_web_lg")

        return CustomSpacy.nlp


def get_spacy() -> Language:
    return CustomSpacy.get_spacy()