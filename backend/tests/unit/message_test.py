import pytest

from lib.nlu.message import MessageValidationCode, Message
from tests.common import queries, spacy, message_builder


@pytest.mark.parametrize("query", queries)
# This test checks whether the intents from the annotated queries are all valid.
def test_message_validation(query):
    new_sent = spacy(query["query"])[:]
    message = message_builder.create_message(new_sent)
    assert Message.validate_message(message) not in MessageValidationCode.get_server_side_error_codes()