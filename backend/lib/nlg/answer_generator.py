import decimal
import pathlib
import random
import re
from typing import Tuple

import yaml

from lib.database.querier import QueryResultCode, QueryResult
from lib.nlu.intent import Intent, ValueType
from lib.nlu.message import Message, MessageValidationCode
from lib.nlu.slot import Slots
from lib.nlu.slot.date import Date
from lib.nlu.slot.location import Location


class AnswerGenerator:
    """Class that provides methods to generate an answer in natural language.

    The answer patterns used by this class will be read from the answers.yaml file. The patterns im the answers.yaml
    file must be provided for each possible combination of intent. It is currently not possible to reuse other patterns,
    so each combination must be added manually.

    Words wrapped in curly brackets, for example "{location}", allow to
    specify the fields that must be passed on to the answer pattern. It is also possible to define optional fields
    by wrapping the field including any additional text in <>. For example, let's consider the pattern
    "There have been {number} cases< in {location}>.". In this case, "number" is a mandatory field, so it must be passed
    as a parameter. The location paramter is wrapped in <>, meaning that it is optional. Furthermore, the word "in" is
    also inside the <> brackets. This means that in the event that no location parameter is passed to the answer
    generator, the "in" will be omitted as well. So two possible answer generated from this pattern might be
    "There have been 1,000 cases." and "There have been 1,000 cases in Austria.".
    """
    def __init__(self):
        with open(pathlib.Path(__file__).parent / "answers.yaml") as answers_file:
            self.answers: dict = yaml.safe_load(answers_file)

    def generate_answer(self, query_result: QueryResult) -> str:
        """Generates an answer based on a QueryResult object."""
        if query_result.result_code == QueryResultCode.NO_DATA_AVAILABLE_FOR_DATE:
            # Latest date contains the most recent date for which we have information available.
            return random.choice(self.answers[query_result.result_code.NO_DATA_AVAILABLE_FOR_DATE.name]).format(
                date=query_result.message.slots.date,
                latest_date=Date.generate_date_message(query_result.information["latest"], include_preposition=False),
                location=Location.add_prepositions_to_location_name(query_result.information["location"]),
                topic=query_result.message.topic.name.lower()
            )
        elif query_result.result_code in [QueryResultCode.UNEXPECTED_RESULT,
                                          QueryResultCode.FUTURE_DATA_REQUESTED]:
            return random.choice(self.answers[query_result.result_code.name])
        elif query_result.result_code == QueryResultCode.NOT_EXISTING_LOCATION:
            return random.choice(self.answers[query_result.result_code.name]).format(location=query_result.message.slots.location)
        elif query_result.result_code == QueryResultCode.INVALID_MESSAGE:
            # Check whether the invalid message is due to a user error or a not considered case server-side.
            if query_result.information["message_validation_code"] in MessageValidationCode.get_user_query_error_codes():
                return random.choice(self.answers[query_result.result_code.name][query_result.information["message_validation_code"].name])
            else:
                # An unconsidered case occurred, maybe a special combination of the various fields for the intent.
                return random.choice(self.answers[query_result.result_code.name]["INTERNAL_ERROR"])
        elif query_result.result_code == QueryResultCode.SUCCESS:
            return self._generate_success_answer(query_result)
        else:
            raise NotImplementedError()

    def _generate_success_answer(self, query_result: QueryResult) -> str:
        """Generates an answer based on the assumption that the query was successful."""
        message: Message = query_result.message
        sub_fields: dict = self._get_sub_fields_from_slots_for_success_message(query_result)

        unformatted_answer: str = random.choice(self.answers["SUCCESS"][message.intent.value_domain.name]
                                 [message.intent.value_type.name][message.intent.calculation_type.name]
                                 [message.intent.measurement_type.name])

        # Remove opional fields if they are not in the parameters
        if "location" not in sub_fields:
            unformatted_answer = re.sub(r"<[^<]*{location}[^>]*>", "", unformatted_answer)
        if "date" not in sub_fields:
            unformatted_answer = re.sub(r"<[^<]*{date}[^>]*>", "", unformatted_answer)

        unformatted_answer = re.sub(r"<|>", "", unformatted_answer)

        try:
            return unformatted_answer.format(**sub_fields)
        except KeyError:
            # We tried to format with a key that doesn't exist in the answer pattern
            raise NotImplementedError()

    def _get_sub_fields_from_slots_for_success_message(self, query_result: QueryResult) -> dict:
        """Extracts the additional information from the query results into a dict."""
        slots: Slots = query_result.message.slots
        result = query_result.result
        value_dict = dict()

        if result is not None:
            # Format integers properly
            if isinstance(result, (int, float, decimal.Decimal)):
                value_dict["result"] = f"{int(result):,}"
            else:
                value_dict["result"] = str(result)

        location = query_result.information["location"] if "location" in query_result.information else None

        if location:
            value_dict["location"] = Location.add_prepositions_to_location_name(location)

        if slots.date:
            value_dict["date"] = Date.generate_date_message(slots.date)

        return value_dict

