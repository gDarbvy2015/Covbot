from lib.database.querier import Querier
from lib.nlg.answer_generator import AnswerGenerator
from lib.nlu.message import MessageBuilder
from lib.spacy_components.custom_spacy import get_spacy

message_builder = MessageBuilder()
querier = Querier()
answer_generator = AnswerGenerator()
spacy = get_spacy()
print("Finished initialization!")

if __name__ == '__main__':
    while True:
        question = input("> ")

        if question == "quit":
            break

        sentence = list(spacy(question).sents)[0]
        message = message_builder.create_message(sentence)
        query_result = querier.query_intent(message)
        answer = answer_generator.generate_answer(query_result)
        print(answer)