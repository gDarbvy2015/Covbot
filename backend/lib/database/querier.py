from typing import Tuple, Any, Union, List

from lib.database.database_connection import DatabaseConnection
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.sql.selectable import Select
from entities import Case, Vaccination
from lib.intention.intent_recognizer import IntentRecognizer
from lib.intention.intent import Intent, Topic, Area, TimeFrame, Datapoint


class Querier:
    def __init__(self):
        self.engine = DatabaseConnection().create_engine("covbot")
        self.session = Session(self.engine, future=True)

    def get_results(self, intent: Intent) -> Any:
        selected_table = self._get_table(intent)
        if selected_table is None:
            return intent, None

        filtered_location = self._filter_location(intent, selected_table)
        filtered_time = self._filter_time_frame(intent, filtered_location)
        results = self.session.execute(filtered_time).scalars().all()

        wanted_value = self._get_wanted_value(intent, results)

        return wanted_value

    def _get_wanted_value(self, intent: Intent, results: List) -> Any:
        if intent.datapoint["type"] == Datapoint.NUMBER:
            return results[0].cases
        else:
            raise NotImplementedError()

    def _filter_time_frame(self, intent: Intent, selection: Select) -> Select:
        if intent.time_frame["type"] == TimeFrame.SINGLE_DAY:
            return selection.filter_by(date=intent.time_frame["date"])
        else:
            raise NotImplementedError()

    def _filter_location(self, intent: Intent, selection: Select) -> Select:
        if intent.area["type"] == Area.ONE_COUNTRY:
            return selection.filter_by(country_normalized=intent.area["country"])
        else:
            raise NotImplementedError()

    def _get_table(self, intent: Intent) -> Union[Select, None]:
        if intent.topic["type"] == Topic.NOT_SPECIFIED:
            return None
        elif intent.topic["type"] == Topic.SINGLE_TOPIC:
            if intent.topic["topic"] == "cases":
                return select(Case)
            else:
                return select(Vaccination)
        elif intent.topic["type"] == Topic.MULTIPLE_TOPICS:
            raise NotImplementedError()
        else:
            raise NotImplementedError()


if __name__ == '__main__':
    sent1 = "How many people were infected on November 27th 2021 in Austria?"

    querier = Querier()

    ir = IntentRecognizer()
    sent1_intention = ir.get_intent(sent1)
    print(sent1_intention)
    result = querier.get_results(sent1_intention)
    print(result)
