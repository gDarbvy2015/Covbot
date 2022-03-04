import pathlib
import random
import re
from typing import Tuple

import yaml

from lib.database.querier import QueryResultCode, QueryResult
from lib.nlu.message import Message
from lib.nlu.slot import Slots
from lib.nlu.slot.date import Date


class AnswerGenerator:
    def __init__(self):
        with open(pathlib.Path(__file__).parent / "answers.yaml") as answers_file:
            self.answers: dict = yaml.safe_load(answers_file)

    def generate_answer(self, query_result: QueryResult) -> str:

        if query_result.result_code in [QueryResultCode.UNKNOWN_TOPIC, QueryResultCode.UNKNOWN_VALUE_TYPE, QueryResultCode.UNKNOWN_VALUE_DOMAIN,
                                        QueryResultCode.UNKNOWN_CALCULATION_TYPE, QueryResultCode.UNKNOWN_MEASUREMENT_TYPE]:
            return random.choice(self.answers[QueryResultCode.UNKNOWN_TOPIC.name])
        elif query_result.result_code in [QueryResultCode.NO_DATA_AVAILABLE_FOR_DATE, QueryResultCode.UNEXPECTED_RESULT,
                                          QueryResultCode.FUTURE_DATA_REQUESTED]:
            return random.choice(self.answers[query_result.result_code.name])
        elif query_result.result_code == QueryResultCode.NOT_EXISTING_LOCATION:
            return random.choice(self.answers[query_result.result_code.name]).format(location=query_result.message.slots)
        elif query_result.result_code == QueryResultCode.SUCCESS:
            return self._generate_success_answer(query_result)
        else:
            raise NotImplementedError()

    def _generate_success_answer(self, query_result: QueryResult) -> str:
        message: Message = query_result.message
        sub_fields: dict = self._get_sub_fields_from_slots_for_success_message(query_result)

        unformatted_answer: str = random.choice(self.answers["SUCCESS"][message.intent.value_domain.name]
                                 [message.intent.value_type.name][message.intent.calculation_type.name]
                                 [message.intent.measurement_type.name])

        if "location" not in sub_fields:
            unformatted_answer = re.sub(r"<[^<]*{location}[^>]*>", "", unformatted_answer)
        if "date" not in sub_fields:
            unformatted_answer = re.sub(r"<[^<]*{date}[^>]*>", "", unformatted_answer)

        unformatted_answer = re.sub(r"<|>", "", unformatted_answer)

        try:
            return unformatted_answer.format(**sub_fields)
        except KeyError:
            raise NotImplementedError()

    def _get_sub_fields_from_slots_for_success_message(self, query_result: QueryResult) -> dict:
        slots: Slots = query_result.message.slots
        result = query_result.result
        if slots.location is None:
            if slots.date is None:
                return {"result": result}
            else:
                return {"result": result, "date": Date.generate_date_message(slots.date)}
        else:
            if slots.date is None:
                return {"result": result, "location": slots.location}
            else:
                return {"result": result, "date": Date.generate_date_message(slots.date), "location": slots.location}

if __name__ == '__main__':
    with open(pathlib.Path(__file__).parent / "answers.yaml") as answers_file:
        entries = yaml.safe_load(answers_file)

