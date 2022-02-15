import unittest
import json
from lib.nlu.topic import TopicRecognizer, Topic
from lib.spacy_components.spacy import get_spacy


class TestQueryTopics(unittest.TestCase):
    def setUp(self):
        self.spacy = get_spacy()
        with open("annotated_queries.json") as query_file:
            self.queries = json.load(query_file)

    def test_topics(self):
        for query in self.queries:
            with self.subTest(query=query):
                predicted_topic = self.spacy(query["query"])._.topic
                self.assertEqual(Topic.from_str(query["topic"]), predicted_topic)
