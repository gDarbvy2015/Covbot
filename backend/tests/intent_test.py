import pathlib
import json
import pytest

from lib.nlu.intent.calculation_type import CalculationType
from lib.nlu.intent.intent import IntentRecognizer
from lib.nlu.intent.measurement_type import MeasurementType
from lib.nlu.intent.value_domain import ValueDomain
from lib.nlu.intent.value_type import ValueType
from lib.spacy_components.spacy import get_spacy

with open(pathlib.Path(__file__).parent / "annotated_queries.json") as query_file:
    queries = json.load(query_file)

spacy = get_spacy()
intent_recognizer = IntentRecognizer(spacy.vocab)


@pytest.mark.parametrize("query", queries)
def test_value_domain(query):
    if not query["id"] == 21:
        doc = spacy(query["query"])
        predicted_value_domain = intent_recognizer.recognize_value_domain(list(doc.sents)[0])
        assert ValueDomain.from_str(query["intent"]["value_domain"]) == predicted_value_domain


@pytest.mark.parametrize("query", queries)
def test_calculation_type(query):
    doc = spacy(query["query"])
    predicted_calculation_type = intent_recognizer.recognize_calculation_type(list(doc.sents)[0])
    assert CalculationType.from_str(query["intent"]["calculation_type"]) == predicted_calculation_type


@pytest.mark.parametrize("query", queries)
def test_measurement_type(query):
    doc = spacy(query["query"])
    predicted_measurement_type = intent_recognizer.recognize_measurement_type(list(doc.sents)[0])
    assert MeasurementType.from_str(query["intent"]["measurement_type"]) == predicted_measurement_type


@pytest.mark.parametrize("query", queries)
def test_value_type(query):
    doc = spacy(query["query"])
    predicted_value_type = intent_recognizer.recognize_value_type(list(doc.sents)[0])
    assert ValueType.from_str(query["intent"]["value_type"]) == predicted_value_type
