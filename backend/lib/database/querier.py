from dataclasses import dataclass

from lib.database.database_connection import DatabaseConnection
from sqlalchemy.orm import Session
from enum import Enum
from lib.spacy_components.spacy import get_spacy

from lib.nlu.intent import Intent, IntentRecognizer


class QueryErrorCode(Enum):
    pass


@dataclass
class QueryError:
    intent: Intent
    error_code: QueryErrorCode
    information: dict


class Querier:
    def __init__(self):
        self.engine = DatabaseConnection().create_engine("covbot")
        self.session = Session(self.engine, future=True)


if __name__ == '__main__':
    sentence = "How many people have been vaccinated in Europe on August 25th 2021"
    spacy = get_spacy()
    doc = spacy(sentence)
    intent_recognizer = IntentRecognizer(spacy.vocab)
    print(type(list(doc.sents)[0]))
    intent = intent_recognizer.recognize_intent(list(doc.sents)[0])
    print(intent)