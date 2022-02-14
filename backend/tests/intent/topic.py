import unittest

from lib.intention.intent import Topic
from lib.intention.intent_recognizer import IntentRecognizer


class TestTopicRecognition(unittest.TestCase):
    def setUp(self):
        self.intent_recognizer = IntentRecognizer()

    def test_topic_vaccination_1(self):
        msg = "How many people have been vaccinated?"
        topic = self.intent_recognizer.get_topic(msg)
        self.assertIs(topic["type"], Topic.SINGLE_TOPIC)
        self.assertIs(topic["topic"], "vaccinations")

    def test_topic_vaccination_2(self):
        msg = "Which country administered got the most shots?"
        topic = self.intent_recognizer.get_topic(msg)
        self.assertIs(topic["type"], Topic.SINGLE_TOPIC)
        self.assertIs(topic["topic"], "vaccinations")

    def test_topic_vaccination_3(self):
        msg = "When have most of the vaccinations been administered in Austria?"
        topic = self.intent_recognizer.get_topic(msg)
        self.assertIs(topic["type"], Topic.SINGLE_TOPIC)
        self.assertIs(topic["topic"], "vaccinations")

    def test_topic_cases_1(self):
        msg = "How many new cases have been reported today?"
        topic = self.intent_recognizer.get_topic(msg)
        self.assertIs(topic["type"], Topic.SINGLE_TOPIC)
        self.assertIs(topic["topic"], "cases")

    def test_topic_cases_2(self):
        msg = "How many positive COVID tests did we have yesterday?"
        topic = self.intent_recognizer.get_topic(msg)
        self.assertIs(topic["type"], Topic.SINGLE_TOPIC)
        self.assertIs(topic["topic"], "cases")

    def test_topic_cases_3(self):
        msg = "How many people caught COVID today?"
        topic = self.intent_recognizer.get_topic(msg)
        self.assertIs(topic["type"], Topic.SINGLE_TOPIC)
        self.assertIs(topic["topic"], "cases")

    def test_topic_cases_4(self):
        msg = "How many people got COVID today?"
        topic = self.intent_recognizer.get_topic(msg)
        self.assertIs(topic["type"], Topic.SINGLE_TOPIC)
        self.assertIs(topic["topic"], "cases")

