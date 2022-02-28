import pathlib
import json
import pytest

from lib.nlu.slot.location import LocationRecognizer
from lib.spacy_components.custom_spacy import get_spacy

with open(pathlib.Path(__file__).parent / "annotated_queries.json") as query_file:
    queries = json.load(query_file)

spacy = get_spacy()
location_recognizer = LocationRecognizer()


@pytest.mark.parametrize("query", queries)
def test_locations(query):
        doc = spacy(query["query"])
        recognized_location = location_recognizer.recognize_location(list(doc.sents)[0])
        assert query["slots"]["location"] == recognized_location
