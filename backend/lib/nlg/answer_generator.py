import pathlib
import random
import re
from typing import Tuple

import yaml

from lib.database.querier import QueryResultCode, QueryResult
from lib.nlu.intent import Intent
from lib.nlu.message import Message, MessageValidationCode
from lib.nlu.slot import Slots
from lib.nlu.slot.date import Date


class AnswerGenerator:
    def __init__(self):
        with open(pathlib.Path(__file__).parent / "answers.yaml") as answers_file:
            self.answers: dict = yaml.safe_load(answers_file)

    def generate_answer(self, query_result: QueryResult) -> str:

        if query_result.result_code in [QueryResultCode.NO_DATA_AVAILABLE_FOR_DATE, QueryResultCode.UNEXPECTED_RESULT,
                                          QueryResultCode.FUTURE_DATA_REQUESTED]:
            return random.choice(self.answers[query_result.result_code.name])
        elif query_result.result_code == QueryResultCode.NOT_EXISTING_LOCATION:
            return random.choice(self.answers[query_result.result_code.name]).format(location=query_result.message.slots.location)
        elif query_result.result_code == QueryResultCode.INVALID_MESSAGE:
            if query_result.information["message_validation_code"] in MessageValidationCode.get_user_query_error_codes():
                return random.choice(self.answers[query_result.result_code.name][query_result.information["message_validation_code"].name])
            else:
                return random.choice(self.answers[query_result.result_code.name]["INTERNAL_ERROR"])
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
        value_dict = dict()

        if result is not None:
            value_dict["result"] = str(result)

        if slots.location:
            value_dict["location"] = slots.location

        if slots.date:
            value_dict["date"] = Date.generate_date_message(slots.date)

        return value_dict

if __name__ == '__main__':
    with open(pathlib.Path(__file__).parent / "answers.yaml") as answers_file:
        entries = yaml.safe_load(answers_file)

