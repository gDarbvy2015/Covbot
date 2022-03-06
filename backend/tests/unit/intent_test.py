import json
import pathlib

import pytest

from lib.nlu.intent import IntentRecognizer, ValueDomain, CalculationType, MeasurementType, ValueType
from tests.common import queries, spacy, intent_recognizer


@pytest.mark.parametrize("query", queries)
def test_value_domain(query):
    doc = spacy(query["query"])
    predicted_value_domain = intent_recognizer.recognize_value_domain(doc[:])
    assert predicted_value_domain == ValueDomain.from_str(query["intent"]["value_domain"])


@pytest.mark.parametrize("query", queries)
def test_calculation_type(query):
    doc = spacy(query["query"])
    predicted_calculation_type = intent_recognizer.recognize_calculation_type(doc[:])
    assert predicted_calculation_type == CalculationType.from_str(query["intent"]["calculation_type"])


@pytest.mark.parametrize("query", queries)
def test_measurement_type(query):
    doc = spacy(query["query"])
    predicted_measurement_type = intent_recognizer.recognize_measurement_type(doc[:])
    assert predicted_measurement_type == MeasurementType.from_str(query["intent"]["measurement_type"])


@pytest.mark.parametrize("query", queries)
def test_value_type(query):
    doc = spacy(query["query"])
    predicted_value_type = intent_recognizer.recognize_value_type(doc[:])
    assert predicted_value_type == ValueType.from_str(query["intent"]["value_type"])
