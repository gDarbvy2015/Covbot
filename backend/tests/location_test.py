import pathlib
import unittest
import json

from lib.nlu.location import LocationRecognizer
from lib.nlu.topic import Topic
from lib.spacy_components.spacy import get_spacy


class TestLocation(unittest.TestCase):
    def setUp(self):
        self.spacy = get_spacy()
        self.location_recognizer = LocationRecognizer()
        with open(pathlib.Path(__file__) / ".." / "annotated_queries.json") as query_file:
            self.queries = json.load(query_file)

    def test_locations(self):
        for query in self.queries:
            with self.subTest(query=query):
                doc = self.spacy(query["query"])
                recognized_location = self.location_recognizer.recognize_location(list(doc.sents)[0])
                self.assertEqual(query["slots"]["location"], recognized_location)
