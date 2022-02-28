import pathlib
import unittest
import json
import pytest
from lib.nlu.topic.topic import TopicRecognizer, Topic
from lib.spacy_components.custom_spacy import get_spacy

with open(pathlib.Path(__file__).parent / "annotated_queries.json") as query_file:
    queries = json.load(query_file)

spacy = get_spacy()
topic_recognizer = TopicRecognizer()


@pytest.mark.parametrize("query", queries)
def test_topics(query):
    doc = spacy(query["query"])
    predicted_topic = topic_recognizer.recognize_topic(list(doc.sents)[0])
    assert Topic.from_str(query["topic"]) == predicted_topic
