import unittest
import json
from lib.nlu.topic import TopicRecognizer, Topic


class TestQueryTopics(unittest.TestCase):
    def setUp(self):
        self.topic_recognizer = TopicRecognizer()
        with open("annotated_queries.json") as query_file:
            self.queries = json.load(query_file)

        print(self.queries)

    def test_topics(self):
        for query in self.queries:
            with self.subTest(query=query):
                predicted_topic = self.topic_recognizer.recognize_topic(query["query"])
                self.assertEqual(Topic.from_str(query['topic']), predicted_topic)
