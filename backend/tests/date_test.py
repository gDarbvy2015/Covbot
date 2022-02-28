import json
from typing import List, Optional

from spacy import Language
from spacy.tokens import Doc

from lib.nlu.slot.date import DateRecognizer, Date
from lib.spacy_components.custom_spacy import get_spacy
import pathlib
import pytest

with open(pathlib.Path(__file__).parent / "annotated_queries.json") as query_file:
    queries: List[dict] = json.load(query_file)

spacy: Language = get_spacy()
date_recognizer: DateRecognizer = DateRecognizer()


@pytest.mark.parametrize("query", queries)
def test_dates(query):
    doc: Doc = spacy(query["query"])
    predicted_date: Optional[Date] = date_recognizer.recognize_date(list(doc.sents)[0])
    if predicted_date is None:
        assert query["slots"]["timeframe"] is None
    else:
        assert query["slots"]["timeframe"]["type"] == predicted_date.type
        assert query["slots"]["timeframe"]["text"] == predicted_date.text
        assert predicted_date.value is not None
