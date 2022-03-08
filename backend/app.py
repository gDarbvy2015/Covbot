from flask import Flask, request, jsonify
from flask_cors import CORS

from lib.database.querier import Querier
from lib.nlg.answer_generator import AnswerGenerator
from lib.nlu.message import MessageBuilder
from lib.spacy_components.custom_spacy import CustomSpacy
from lib.util.logger import ServerLogger

app = Flask(__name__)
cors = CORS(app)

message_builder: MessageBuilder = MessageBuilder()
querier: Querier = Querier()
answer_generator: AnswerGenerator = AnswerGenerator()
spacy = CustomSpacy.get_spacy()
logger: ServerLogger = ServerLogger(__name__)
logger.info("Successfully started the web server... Starting listening to requests now.")

@app.route('/')
def get_reply():  # put application's code here
    raw_message: str = request.args.get("msg", default="")
    try:
        logger.info(f"Received a new message {raw_message.__repr__()}.")
        message = message_builder.create_message(spacy(raw_message)[:])
        logger.info(f"Successfully converted the message to {message}.")
        query_result = querier.query_intent(message)
        logger.info(f"Successfully queried the message with the result {query_result}.")
        answer = answer_generator.generate_answer(query_result)
        logger.info(f"Successfully generated the answer {answer.__repr__()}.")
        return jsonify({"msg": answer})
    except Exception:
        logger.exception(f"Erorr occurred while processing the message {raw_message.__repr__()}")
        raise


if __name__ == '__main__':
    app.run()
