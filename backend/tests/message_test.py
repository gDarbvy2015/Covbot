import json
import pathlib

import pytest

from lib.nlu.message import MessageBuilder, MessageValidationCode, Message
from lib.spacy_components.custom_spacy import get_spacy

with open(pathlib.Path(__file__).parent / "annotated_queries.json") as query_file:
    queries = json.load(query_file)

spacy = get_spacy()
message_builder = MessageBuilder()


@pytest.mark.parametrize("query", queries)
# This test checks whether the intents from the annotated queries are all valid.
def test_message_validation(query):
    new_sent = list(spacy(query["query"]).sents)[0]
    message = message_builder.create_message(new_sent)
    assert Message.validate_message(message) not in MessageValidationCode.get_server_side_error_codes()