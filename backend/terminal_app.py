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

    sentences = [
        #"How many new cases have been reported in Austria yesterday?",
        #"Tell me the number of COVID cases in Germany on 28.02.2022",
        #"number of COVID cases in Serbia on 28.02.2022",
        #"What is the peak number of confirmed cases in Germany",
        #"What is the lowest number of confirmed cases in Australia",
        #"What is the highest number of people vaccinated in Australia",
        "How many new Covid cases are there in the UK today?"
    ]

    for sentence in sentences:
        new_sent = list(spacy(sentence).sents)[0]
        message = message_builder.create_message(new_sent)
        query_result = querier.query_intent(message)
        answer = answer_generator.generate_answer(query_result)
        print(sentence)
        print(answer)
        print()


    # while True:
    #     question = input("> ")
    #
    #     if question == "quit":
    #         break
    #
    #     sentence = list(spacy(question).sents)[0]
    #     message = message_builder.create_message(sentence)
    #     query_result = querier.query_intent(message)
    #     answer = answer_generator.generate_answer(query_result)
    #     print(answer)
