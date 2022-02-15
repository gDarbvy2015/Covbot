import unittest
import json
from lib.nlu.intent import Intent, IntentRecognizer


class TestQueryIntents(unittest.TestCase):
    def setUp(self):
        self.intent_recognizer = IntentRecognizer()
        with open("annotated_queries.json") as query_file:
            self.queries = [query for query in json.load(query_file)
                            if Intent.from_str(query["intent"]) == Intent.DAILY_POSITIVE_CASES]

    def test_intents(self):
        for query in self.queries:
            with self.subTest(query=query):
                predicted_intent = self.intent_recognizer.recognize_intent(query["query"])
                self.assertEqual(Intent.from_str(query['intent']), predicted_intent)
