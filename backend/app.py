from flask import Flask, request, jsonify
from flask_cors import CORS

from lib.database.querier import Querier
from lib.nlg.answer_generator import AnswerGenerator
from lib.nlu.message import MessageBuilder
from lib.spacy_components.custom_spacy import CustomSpacy

app = Flask(__name__)
cors = CORS(app)

message_builder: MessageBuilder = MessageBuilder()
querier: Querier = Querier()
answer_generator: AnswerGenerator = AnswerGenerator()
spacy = CustomSpacy.get_spacy()

@app.route('/')
def get_reply():  # put application's code here
    message = message_builder.create_message(spacy(request.args.get("msg", default=""))[:])
    query_result = querier.query_intent(message)
    answer = answer_generator.generate_answer(query_result)
    return jsonify({"msg": answer})


if __name__ == '__main__':
    app.run()
