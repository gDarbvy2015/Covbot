import json
import pathlib

from lib.database.querier import Querier
from lib.nlg.answer_generator import AnswerGenerator
from lib.nlu.message import MessageBuilder
from lib.spacy_components.custom_spacy import get_spacy

message_builder = MessageBuilder()
querier = Querier()
answer_generator = AnswerGenerator()
spacy = get_spacy()

if __name__ == '__main__':

    with open(pathlib.Path.cwd() / "tests" / "annotated_queries.json") as query_file:
        queries = json.load(query_file)
    # sentences = [query["query"] for query in queries]

    sentences = ["Which country has had the most corona cases?"]

    for sentence in sentences:
        print(sentence)
        new_sent = list(spacy(sentence).sents)[0]
        print("BEFORE MESSAGE")
        message = message_builder.create_message(new_sent)
        print("BEFORE QUERY")
        query_result = querier.query_intent(message)
        print("BEFORE ANSWER")
        answer = answer_generator.generate_answer(query_result)
        print(answer)
        print()