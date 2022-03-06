import json
import pathlib

import pytest
from spacy.tokens import Doc

from tests.common import queries, spacy, location_recognizer

@pytest.mark.parametrize("query", queries)
def test_locations(query):
    doc: Doc = spacy(query["query"])
    recognized_location: str = location_recognizer.recognize_location(doc[:])
    assert recognized_location == query["slots"]["location"]
