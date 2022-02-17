import unittest
import json
from lib.nlu.intent import Intent, IntentRecognizer
from lib.spacy_components.spacy import get_spacy


class TestQueryIntents(unittest.TestCase):
    def setUp(self):
        self.spacy = get_spacy()
        with open("annotated_queries.json") as query_file:
            self.queries = [query for query in json.load(query_file)
                            if Intent.from_str(query["intent"]["datapoint"]) == Intent.DAILY_POSITIVE_CASES or
                            Intent.from_str(query["intent"]["datapoint"]) == Intent.CUMULATIVE_POSITIVE_CASES]

    def test_daily_positive_cases_intents(self):
        for query in self.queries:
            with self.subTest(query=query):
                predicted_intent = self.spacy(query["query"])._.intent
                self.assertEqual(Intent.from_str(query["intent"]["datapoint"]), predicted_intent)
