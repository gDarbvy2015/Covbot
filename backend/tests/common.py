import json
import pathlib

from lib.database.querier import Querier
from lib.nlg.answer_generator import AnswerGenerator
from lib.nlu.intent import IntentRecognizer
from lib.nlu.message import MessageBuilder
from lib.nlu.slot.date import DateRecognizer
from lib.nlu.slot.location import LocationRecognizer
from lib.nlu.topic import TopicRecognizer
from lib.spacy_components.custom_spacy import get_spacy


with open(pathlib.Path(__file__).parent / "annotated_queries.json") as query_file:
    queries = json.load(query_file)

spacy = get_spacy()
intent_recognizer = IntentRecognizer(spacy.vocab)
location_recognizer = LocationRecognizer()
topic_recognizer = TopicRecognizer()
querier = Querier()
message_builder = MessageBuilder()
answer_generator = AnswerGenerator()
date_recognizer = DateRecognizer()
