import unittest
import json
from lib.nlu.intent import Intent, IntentRecognizer, ValueDomain
from lib.spacy_components.spacy import get_spacy


class TestQueryIntents(unittest.TestCase):
    def setUp(self):
        self.spacy = get_spacy()
        with open("annotated_queries.json") as query_file:
            self.queries = [query for query in json.load(query_file)
                            if query["intent"]["value_domain"] == "VACCINATED_PEOPLE"]

    def test_value_domain(self):
        for query in self.queries:
            with self.subTest(query=query):
                predicted_value_domain = self.spacy(query["query"])._.intent.value_domain
                self.assertEqual(ValueDomain.from_str(query["intent"]["value_domain"]), predicted_value_domain)
