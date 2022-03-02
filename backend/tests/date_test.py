from datetime import datetime, timedelta
import json
from typing import List, Optional, Tuple

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
today: datetime.date = datetime(2022, 3, 2).date()

date_tuples = [
    (Date("DAY", today, None), "today"),
    (Date("DAY", today - timedelta(days=1), None), "yesterday"),
    (Date("DAY", today + timedelta(days=1), None), "tomorrow"),
    (Date("DAY", today + timedelta(days=2), None), "on March 4th, 2022"),
    (Date("DAY", today - timedelta(days=3), None), "3 days ago"),
    (Date("DAY", today - timedelta(days=8), None), "on February 22nd, 2022"),
]


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


@pytest.mark.parametrize("date_tuple", date_tuples)
def test_date_to_string(date_tuple: Tuple):
    assert Date.generate_date_message(date_tuple[0]) == date_tuple[1]
