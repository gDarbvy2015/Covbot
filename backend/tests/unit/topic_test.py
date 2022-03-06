import json
import pathlib
from typing import List

import pytest
from spacy import Language
from spacy.tokens import Doc

from lib.nlu.topic import TopicRecognizer, Topic
from tests.common import queries, spacy, topic_recognizer


@pytest.mark.parametrize("query", queries)
def test_topics(query):
    doc: Doc = spacy(query["query"])
    predicted_topic: Topic = topic_recognizer.recognize_topic(doc[:])
    assert predicted_topic == Topic.from_str(query["topic"])
