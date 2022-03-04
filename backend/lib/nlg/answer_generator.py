import pathlib
import random
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
        sub_fields: Tuple[str, dict] = self._get_sub_fields_from_slots(query_result.message.slots)

        if query_result.result_code in [QueryResultCode.UNKNOWN_TOPIC, QueryResultCode.UNKNOWN_VALUE_TYPE, QueryResultCode.UNKNOWN_VALUE_DOMAIN,
                                        QueryResultCode.UNKNOWN_CALCULATION_TYPE, QueryResultCode.UNKNOWN_MEASUREMENT_TYPE]:
            return random.choice(self.answers[QueryResultCode.UNKNOWN_TOPIC.name]["NONE"])
        elif query_result.result_code in [QueryResultCode.NO_DATA_AVAILABLE_FOR_DATE, QueryResultCode.UNEXPECTED_RESULT,
                                          QueryResultCode.FUTURE_DATA_REQUESTED]:
            return random.choice(self.answers[query_result.result_code.name]["NONE"])
        elif query_result.result_code ==  QueryResultCode.NOT_EXISTING_LOCATION:
            return random.choice(self.answers[query_result.result_code.name]["LOCATION"])
        elif query_result.result_code == QueryResultCode.SUCCESS:
            return self._generate_success_answer(query_result, sub_fields)
        else:
            raise NotImplementedError()

    def _get_sub_fields_from_slots(self, slots: Slots) -> Tuple[str, dict]:
        if slots.location is None:
            if slots.date is None:
                return "NONE", {}
            else:
                return "DATE", {"date": Date.generate_date_message(slots.date)}
        else:
            if slots.date is None:
                return "LOCATION", {"location": slots.location}
            else:
                return "DATE_AND_LOCATION", {"date": Date.generate_date_message(slots.date), "location": slots.location}

    def _generate_success_answer(self, query_result: QueryResult, sub_fields: Tuple[str, dict]) -> str:
        message: Message = query_result.message
        sub_fields[1]["result"] = query_result.result

        try:
            return random.choice(self.answers["SUCCESS"][message.intent.value_domain.name]
                                 [message.intent.value_type.name][message.intent.calculation_type.name]
                                 [message.intent.measurement_type.name][sub_fields[0]]).format(**sub_fields[1])
        except KeyError:
            raise NotImplementedError()

if __name__ == '__main__':
    with open(pathlib.Path(__file__).parent / "answers.yaml") as answers_file:
        entries = yaml.safe_load(answers_file)

