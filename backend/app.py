import time

from flask import Flask, request, jsonify
from flask_cors import CORS

from lib.database.querier import Querier
from lib.nlg.answer_generator import AnswerGenerator
from lib.nlu.message import MessageBuilder
from lib.spacy_components.custom_spacy import CustomSpacy
from lib.util.logger import ServerLogger, MessageLogger
from lib.database.dataset_updater import DatasetUpdater
import threading

app = Flask(__name__)
cors = CORS(app)

message_builder: MessageBuilder = MessageBuilder()
querier: Querier = Querier()
answer_generator: AnswerGenerator = AnswerGenerator()
spacy = CustomSpacy.get_spacy()
server_logger: ServerLogger = ServerLogger(__name__)
server_logger.info("Successfully started the web server... Starting listening to requests now.")
message_logger: MessageLogger = MessageLogger(__name__)
dataset_updater: DatasetUpdater = DatasetUpdater()


def start_dataset_updater_loop():
    while True:
        dataset_updater.start()
        server_logger.info("Waiting 2 hours before attempting the next update...")
        time.sleep(10)


t1 = threading.Thread(target=start_dataset_updater_loop)
t1.start()


@app.route('/')
def get_reply():  # put application's code here
    raw_message: str = request.args.get("msg", default="")
    try:
        server_logger.info(f"Received a new message {raw_message.__repr__()}.")
        message = message_builder.create_message(spacy(raw_message)[:])
        server_logger.info(f"Successfully converted the message to {message}.")
        query_result = querier.query_intent(message)
        server_logger.info(f"Successfully queried the message with the result {query_result}.")
        answer = answer_generator.generate_answer(query_result)
        server_logger.info(f"Successfully generated the answer {answer.__repr__()}.")
        message_logger.info(f"QUERY: {raw_message}; ANSWER: {answer}")
        return jsonify({"msg": answer})
    except Exception:
        server_logger.exception(f"Error occurred while processing the message {raw_message.__repr__()}")
        message_logger.info(f"QUERY: {raw_message}; ANSWER: ERROR")
        raise


if __name__ == '__main__':
    app.run()
    print("Reached")
