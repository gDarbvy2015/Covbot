import unittest
import json

from lib.nlu.slot.date import DateRecognizer
from lib.spacy_components.spacy import get_spacy
import pathlib


class TestQueryTopics(unittest.TestCase):
    def setUp(self):
        self.spacy = get_spacy()
        self.date_recognizer = DateRecognizer()
        with open(pathlib.Path(__file__) / ".." / "annotated_queries.json") as query_file:
            self.queries = json.load(query_file)

    def test_topics(self):
        for query in self.queries:
            with self.subTest(query=query):
                doc = self.spacy(query["query"])
                predicted_date = self.date_recognizer.recognize_date(list(doc.sents)[0])
                if predicted_date is None:
                    self.assertEqual(query["slots"]["timeframe"], None)
                else:
                    self.assertEqual(query["slots"]["timeframe"]["type"], predicted_date.type)
                    self.assertEqual(query["slots"]["timeframe"]["value"], predicted_date.original_string)
                    self.assertNotEqual(predicted_date.value, None)
