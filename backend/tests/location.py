import unittest
import json
from lib.nlu.topic import Topic
from lib.spacy_components.spacy import get_spacy


class TestLocation(unittest.TestCase):
    def setUp(self):
        self.spacy = get_spacy()
        with open("annotated_queries.json") as query_file:
            self.queries = json.load(query_file)

    def test_locations(self):
        for query in self.queries:
            with self.subTest(query=query):
                recognized_location = self.spacy(query["query"])._.location
                self.assertEqual(query["slots"]["location"], recognized_location)
