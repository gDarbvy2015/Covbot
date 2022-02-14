from flask import Flask, jsonify, request
from flask_cors import CORS

from lib.database.querier import Querier
from lib.intention.intent_recognizer import IntentRecognizer
from lib.nlp.answer_generator import AnswerGenerator

app = Flask(__name__)
cors = CORS(app)

intent_recognizer = IntentRecognizer()
querier = Querier()
answer_generator = AnswerGenerator()


@app.route('/')
def get_reply():  # put application's code here
    message = request.args.get("message", default="")
    intent = intent_recognizer.get_intent(message)
    result = querier.get_results(intent)
    answer = answer_generator.generate_answer(intent, result)
    return jsonify({"msg": answer})


if __name__ == '__main__':
    app.run()
