from typing import Optional

import spacy
from nltk import PorterStemmer
from spacy.lang.en import Language

from spacy.tokens import Token

stemmer: PorterStemmer = PorterStemmer()

Token.set_extension("stem", getter=lambda t: stemmer.stem(t.lemma_))


class CustomSpacy:
    """Class that provides a method for getting the customized spacy instance."""
    nlp: Optional[Language] = None

    @staticmethod
    def get_spacy() -> Language:
        """Returns the customized spacy instance."""
        if CustomSpacy.nlp is None:
            CustomSpacy.nlp = spacy.load("en_core_web_lg")

        return CustomSpacy.nlp


def get_spacy() -> Language:
    """For compatibility."""
    return CustomSpacy.get_spacy()