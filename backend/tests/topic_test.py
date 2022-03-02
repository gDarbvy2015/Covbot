import json
import pathlib
from typing import List

import pytest
from spacy import Language
from spacy.tokens import Doc

from lib.nlu.topic import TopicRecognizer, Topic
from lib.spacy_components.custom_spacy import get_spacy

with open(pathlib.Path(__file__).parent / "annotated_queries.json") as query_file:
    queries: List[dict] = json.load(query_file)

spacy: Language = get_spacy()
topic_recognizer: TopicRecognizer = TopicRecognizer()


@pytest.mark.parametrize("query", queries)
def test_topics(query):
    doc: Doc = spacy(query["query"])
    predicted_topic: Topic = topic_recognizer.recognize_topic(list(doc.sents)[0])
    assert Topic.from_str(query["topic"]) == predicted_topic
