from __future__ import annotations

import calendar
from dataclasses import dataclass
from datetime import datetime, timedelta, date
from enum import Enum
from typing import Union, Optional, List

from sqlalchemy import and_
from sqlalchemy import desc, asc
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, Query
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql import functions

from lib.database.database_connection import DatabaseConnection
from lib.database.entities import Case, Vaccination
from lib.nlu.intent.calculation_type import CalculationType
from lib.nlu.intent.measurement_type import MeasurementType
from lib.nlu.intent.value_domain import ValueDomain
from lib.nlu.intent.value_type import ValueType
from lib.nlu.message import MessageBuilder, Message
from lib.nlu.topic.topic import Topic
from lib.spacy_components.custom_spacy import get_spacy


class QueryResultCode(Enum):
    SUCCESS = 1
    UNKNOWN_TOPIC = 2
    AMBIGUOUS_TOPIC = 3
    UNKNOWN_MEASUREMENT_TYPE = 4
    UNKNOWN_VALUE_DOMAIN = 5
    UNKNOWN_CALCULATION_TYPE = 6
    UNKNOWN_VALUE_TYPE = 7
    NO_WORLDWIDE_SUPPORTED = 8
    UNEXPECTED_RESULT = 9
    FUTURE_DATA_REQUESTED = 10
    NOT_EXISTING_LOCATION = 11
    NO_DATA_AVAILABLE_FOR_DATE = 12
    UNKNOWN = 13

    @staticmethod
    def from_str(query_result_code: str) -> Optional[QueryResultCode]:
        try:
            return QueryResultCode[query_result_code.upper()]
        except KeyError:
            return QueryResultCode["UNKNOWN"]


@dataclass
class QueryResult:
    message: Message
    result_code: QueryResultCode
    result: Optional[Union[str, int, datetime.date]]
    # In case of an error, we can add a dict with additional information
    information: Optional[dict]


class Querier:
    def __init__(self, db_name="covbot", engine=None, session=None, today=datetime.now().date()):
        self.engine: Engine = DatabaseConnection().create_engine(db_name) if engine is None else engine
        self.session: Session = Session(self.engine, future=True) if session is None else session
        self.case_query: Query = self.session.query(Case)
        self.vaccination_query: Query = self.session.query(Vaccination)

        # We allow setting a custom value as the "today" value so that testing becomes easier
        self.today = today
        self.table_dict: dict = {
            Topic.CASES: Case,
            Topic.VACCINATIONS: Vaccination
        }

        self.column_dict: dict = {
            MeasurementType.DAILY: {
                ValueDomain.POSITIVE_CASES: Case.cases,
                ValueDomain.ADMINISTERED_VACCINES: Vaccination.daily_vaccinations,
                ValueDomain.VACCINATED_PEOPLE: Vaccination.daily_people_vaccinated
            },
            MeasurementType.CUMULATIVE: {
                ValueDomain.POSITIVE_CASES: Case.cumulative_cases,
                ValueDomain.ADMINISTERED_VACCINES: Vaccination.total_vaccinations,
                ValueDomain.VACCINATED_PEOPLE: Vaccination.people_vaccinated
            }
        }

    def query_intent(self, msg: Message) -> QueryResult:
        validation_result: Optional[QueryResult] = self._validate_msg(msg)

        if validation_result:
            return validation_result

        table: Union[Case, Vaccination] = self.table_dict[msg.topic]
        considered_column: InstrumentedAttribute = self.column_dict[msg.intent.measurement_type][
            msg.intent.value_domain]

        if msg.intent.value_type == ValueType.NUMBER:
            return self._query_number(table, considered_column, msg)
        elif msg.intent.value_type == ValueType.LOCATION:
            return self._query_location(table, considered_column, msg)
        elif msg.intent.value_type == ValueType.DAY:
            return self._query_date(table, considered_column, msg)
        else:
            raise NotImplementedError()

    def _query_location(self, table: Union[Case, Vaccination], considered_column: InstrumentedAttribute,
                        msg: Message) -> QueryResult:
        time_condition: List[bool] = self._get_time_from_condition(table, msg)

        if len(self.session.query(table).where(and_(*time_condition)).all()) == 0:
            return QueryResult(msg, QueryResultCode.NO_DATA_AVAILABLE_FOR_DATE, None, None)

        if msg.intent.calculation_type in [CalculationType.MAXIMUM, CalculationType.MINIMUM]:
            sort_order = asc if msg.intent.calculation_type == CalculationType.MINIMUM else desc
            if msg.slots.date is None or msg.slots.date.type == "DAY":
                query = self.session.query(table).where(and_(*time_condition)).order_by(
                    sort_order(considered_column)).limit(1)
                result = query.all()
                if len(result) == 0:
                    return QueryResult(msg, QueryResultCode.UNEXPECTED_RESULT, None, None)
                else:
                    return QueryResult(msg, QueryResultCode.SUCCESS, result[0].country, None)
            else:
                raise NotImplementedError()
        else:
            raise NotImplementedError()

    def _query_date(self, table: Union[Case, Vaccination], considered_column: InstrumentedAttribute,
                    msg: Message) -> QueryResult:
        country_condition: List[bool] = self._get_country_from_condition(table, msg)

        if len(self.session.query(table).where(and_(*country_condition)).all()) == 0:
            return QueryResult(msg, QueryResultCode.NOT_EXISTING_LOCATION, None, {"location": msg.slots.location})

        if msg.intent.calculation_type in [CalculationType.MAXIMUM, CalculationType.MINIMUM]:
            sort_order = asc if msg.intent.calculation_type == CalculationType.MINIMUM else desc
            query = self.session.query(table).where(and_(*country_condition)).order_by(
                sort_order(considered_column)).limit(1)
            result = query.all()
            if len(result) == 0:
                return QueryResult(msg, QueryResultCode.UNEXPECTED_RESULT, None, None)
            else:
                return QueryResult(msg, QueryResultCode.SUCCESS, result[0].date, None)
        else:
            raise NotImplementedError()

    def _query_number(self, table: Union[Case, Vaccination], considered_column: InstrumentedAttribute,
                      msg: Message) -> QueryResult:
        # If no timeframe is given, we assume that the user is asking for today
        time_condition: List[bool] = self._get_time_from_condition(table, msg)
        country_condition: List[bool] = self._get_country_from_condition(table, msg)

        if len(self.session.query(table).where(and_(*country_condition)).all()) == 0:
            return QueryResult(msg, QueryResultCode.NOT_EXISTING_LOCATION, None, {"location": msg.slots.location})

        if len(self.session.query(table).where(and_(*country_condition, *time_condition)).all()) == 0:
            return QueryResult(msg, QueryResultCode.NO_DATA_AVAILABLE_FOR_DATE, None, None)

        if msg.intent.calculation_type == CalculationType.RAW_VALUE:
            query = self.session.query(table).with_entities(considered_column)
        elif msg.intent.calculation_type == CalculationType.SUM:
            query = self.session.query(functions.sum(considered_column))
        elif msg.intent.calculation_type == CalculationType.MAXIMUM:
            query = self.session.query(functions.max(considered_column))
        elif msg.intent.calculation_type == CalculationType.MINIMUM:
            query = self.session.query(functions.min(considered_column))
        else:
            raise NotImplementedError()

        query = query.where(and_(
            *time_condition, *country_condition
        ))

        result = query.all()

        if len(result) > 1:
            return QueryResult(msg, QueryResultCode.UNEXPECTED_RESULT, None, None)
        else:
            return QueryResult(msg, QueryResultCode.SUCCESS, result[0][0], None)

    def _get_country_from_condition(self, table: Union[Case, Vaccination], msg: Message) -> List[bool]:
        if msg.intent.value_type == ValueType.LOCATION:
            return []

        if msg.slots.location is None:
            raise NotImplementedError()
        else:
            return [table.country_normalized == msg.slots.location]

    def _get_time_from_condition(self, table: Union[Case, Vaccination], msg: Message) -> List[bool]:
        if msg.intent.value_type == ValueType.DAY or msg.slots.date is None:
            return []

        date_type: str = msg.slots.date.type
        date_value: datetime.date = msg.slots.date.value
        if date_type == "DAY":
            return [table.date == date_value]
        elif date_type == "WEEK":
            start = date_value - timedelta(days=date_value.weekday())
            end = start + timedelta(days=6)
            return [table.date >= start, table.date <= end]
        elif date_type == "MONTH":
            start = date_value.replace(day=1)
            end = date_value.replace(day=calendar.monthrange(date_value.year, date_value.month)[1])
            return [table.date >= start, table.date <= end]
        elif date_type == "YEAR":
            start = date(date_value.year, 1, 1)
            end = date(date_value.year, 12, 31)
            return [table.date >= start, table.date <= end]
        else:
            raise NotImplementedError()

    def _validate_msg(self, msg: Message) -> Optional[QueryResult]:
        if msg.topic == Topic.UNKNOWN:
            return QueryResult(msg, QueryResultCode.UNKNOWN_TOPIC, None, None)
        if msg.topic == Topic.AMBIGUOUS:
            return QueryResult(msg, QueryResultCode.AMBIGUOUS_TOPIC, None, None)
        if msg.intent.measurement_type == MeasurementType.UNKNOWN:
            return QueryResult(msg, QueryResultCode.UNKNOWN_MEASUREMENT_TYPE, None, None)
        if msg.intent.value_domain == ValueDomain.UNKNOWN:
            return QueryResult(msg, QueryResultCode.UNKNOWN_VALUE_DOMAIN, None, None)
        if msg.intent.calculation_type == CalculationType.UNKNOWN:
            return QueryResult(msg, QueryResultCode.UNKNOWN_CALCULATION_TYPE, None, None)
        if msg.intent.value_type == ValueType.UNKNOWN:
            return QueryResult(msg, QueryResultCode.UNKNOWN_VALUE_TYPE, None, None)
        if msg.slots.date and msg.slots.date.value > self.today:
            return QueryResult(msg, QueryResultCode.FUTURE_DATA_REQUESTED, None, None)
        if msg.intent.value_type != ValueType.LOCATION and msg.slots.location is None:
            return QueryResult(msg, QueryResultCode.NO_WORLDWIDE_SUPPORTED, None, None)

        return None


if __name__ == '__main__':
    sentence = "When were most vaccinations performed in Austria?"
    spacy = get_spacy()
    doc = spacy(sentence)
    querier = Querier()

    mb = MessageBuilder()
    message = mb.create_message(list(doc.sents)[0])
    result = querier.query_intent(message)
    print(result)
