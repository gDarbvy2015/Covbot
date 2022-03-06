import json
import pathlib

import pytest

from tests.common import queries, querier, message_builder, answer_generator, spacy


# This test just checks whether the queries are answered without throwing an error, it doesn't
# check whether the results really are correct.
@pytest.mark.parametrize("query", queries)
def test_whole_pipeline(query):
    new_sent = spacy(query["query"])[:]
    message = message_builder.create_message(new_sent)
    query_result = querier.query_intent(message)
    answer_generator.generate_answer(query_result)
