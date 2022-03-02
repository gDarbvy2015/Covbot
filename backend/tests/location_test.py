import json
import pathlib

import pytest
from spacy.tokens import Doc

from lib.nlu.slot.location import LocationRecognizer
from lib.spacy_components.custom_spacy import get_spacy

with open(pathlib.Path(__file__).parent / "annotated_queries.json") as query_file:
    queries = json.load(query_file)

spacy = get_spacy()
location_recognizer = LocationRecognizer()


@pytest.mark.parametrize("query", queries)
def test_locations(query):
        doc: Doc = spacy(query["query"])
        recognized_location: str = location_recognizer.recognize_location(list(doc.sents)[0])
        assert query["slots"]["location"] == recognized_location
