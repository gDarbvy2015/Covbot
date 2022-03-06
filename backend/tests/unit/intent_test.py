import json
import pathlib

import pytest

from lib.nlu.intent import IntentRecognizer, ValueDomain, CalculationType, MeasurementType, ValueType
from lib.spacy_components.custom_spacy import get_spacy

with open(pathlib.Path(__file__).parent.parent / "annotated_queries.json") as query_file:
    queries = json.load(query_file)

spacy = get_spacy()
intent_recognizer = IntentRecognizer(spacy.vocab)


@pytest.mark.parametrize("query", queries)
def test_value_domain(query):
    doc = spacy(query["query"])
    predicted_value_domain = intent_recognizer.recognize_value_domain(list(doc.sents)[0])
    assert predicted_value_domain == ValueDomain.from_str(query["intent"]["value_domain"])


@pytest.mark.parametrize("query", queries)
def test_calculation_type(query):
    doc = spacy(query["query"])
    predicted_calculation_type = intent_recognizer.recognize_calculation_type(list(doc.sents)[0])
    assert predicted_calculation_type == CalculationType.from_str(query["intent"]["calculation_type"])


@pytest.mark.parametrize("query", queries)
def test_measurement_type(query):
    doc = spacy(query["query"])
    predicted_measurement_type = intent_recognizer.recognize_measurement_type(list(doc.sents)[0])
    assert predicted_measurement_type == MeasurementType.from_str(query["intent"]["measurement_type"])


@pytest.mark.parametrize("query", queries)
def test_value_type(query):
    doc = spacy(query["query"])
    predicted_value_type = intent_recognizer.recognize_value_type(list(doc.sents)[0])
    assert predicted_value_type == ValueType.from_str(query["intent"]["value_type"])
