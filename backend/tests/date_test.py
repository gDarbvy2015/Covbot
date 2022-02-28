import unittest
import json

from lib.nlu.slot.date import DateRecognizer
from lib.spacy_components.custom_spacy import get_spacy
import pathlib
import pytest

with open(pathlib.Path(__file__).parent / "annotated_queries.json") as query_file:
    queries = json.load(query_file)

spacy = get_spacy()
date_recognizer = DateRecognizer()


@pytest.mark.parametrize("query", queries)
def test_topics(query):
    doc = spacy(query["query"])
    predicted_date = date_recognizer.recognize_date(list(doc.sents)[0])
    if predicted_date is None:
        assert query["slots"]["timeframe"] is None
    else:
        assert query["slots"]["timeframe"]["type"] == predicted_date.type
        assert query["slots"]["timeframe"]["value"] == predicted_date.original_string
        assert predicted_date.value is not None
