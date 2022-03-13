from __future__ import annotations

import calendar
from dataclasses import dataclass
from datetime import datetime, timedelta, date
from enum import Enum
from typing import Union, Optional, List

from sqlalchemy import and_, func, not_
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
from lib.nlu.message import MessageBuilder, Message, MessageValidationCode
from lib.nlu.slot.date import Date
from lib.nlu.slot.location import Location
from lib.nlu.topic.topic import Topic
from lib.spacy_components.custom_spacy import get_spacy


class QueryResultCode(Enum):
    """Class representing the result code from a query operation.

    SUCCESS: The query was performed successfully.
    UNEXPECTED_RESULT: The querier received an unexpected return value from the query operation.
    FUTURE_DATA_REQUESTED: It was attempted to query data from the future.
    NOT_EXISTING_LOCATION: It was attempted to search for data on a location that doesn't exist.
    NO_DATA_AVAILABLE_FOR_DATE: It was attempted to query data for a date were no data is available.
    INVALID_MESSAGE: The message that was passed to the querier didn't pass validation (see Message class for
    more details on what constitutes a valid message).
    """
    SUCCESS = 1
    UNEXPECTED_RESULT = 2
    FUTURE_DATA_REQUESTED = 3
    NOT_EXISTING_LOCATION = 4
    NO_DATA_AVAILABLE_FOR_DATE = 5
    INVALID_MESSAGE = 6
    UNSUPPORTED_ACTION = 7
    NO_MAX_MIN_FOR_COUNTRY_SUPPORTED = 9

    @staticmethod
    def from_str(query_result_code: str) -> Optional[QueryResultCode]:
        """Converts a string to a QueryResultCode."""
        try:
            return QueryResultCode[query_result_code.upper()]
        except KeyError:
            return QueryResultCode["UNKNOWN"]


@dataclass
class QueryResult:
    """Class representing the result from a query operation.

    message: Contains the message object that was passed to the querier. This is needed because the AnswerGenerator
    needs to access parts of it for the generation process.
    result_code: The QueryResultCode from the performed query operation.
    result: The actual result value from the query operation.
    information: Any other additional information that is needed for the AnswerGenerator to generate the answer.
    For example, when asking when the highest number of cases was recorded, the result will be the actual date, but we
    also want to pass the location where the highest number was recorded.
    """
    message: Message
    result_code: QueryResultCode
    result: Optional[Union[str, int, datetime.date]]
    # In case of an error, we can add a dict with additional information
    information: dict


class Querier:
    """Class containing helper methods to perform query-related operations."""
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
        """Given a message, it queries the database and returns the result in the form of a QueryResult object."""
        validation_result: Optional[QueryResult] = self._validate_msg(msg)

        # If validation_result is not None, there is an validation error and we return it.
        if validation_result:
            return validation_result

        table: Union[Case, Vaccination] = self.table_dict[msg.topic]
        considered_column = self.column_dict[msg.intent.measurement_type][
            msg.intent.value_domain]

        if msg.intent.value_type == ValueType.NUMBER:
            return self._query_number(table, considered_column, msg)
        elif msg.intent.value_type == ValueType.LOCATION:
            return self._query_location(table, considered_column, msg)
        elif msg.intent.value_type == ValueType.DAY:
            return self._query_date(table, considered_column, msg)
        else:
            return QueryResult(msg, QueryResultCode.UNSUPPORTED_ACTION, None, {})

    def _query_location(self, table: Union[Case, Vaccination], considered_column: InstrumentedAttribute,
                        msg: Message) -> QueryResult:
        """Performs the query given that we are trying to query a location."""
        time_condition: List[bool] = self._get_timeframe_from_condition(table, msg)
        location_condition: List[bool] = self._get_location_from_condition(table, msg)

        if self.session.query(func.count(table.id)).where(and_(*time_condition, *location_condition)).scalar() == 0:
            return QueryResult(msg, QueryResultCode.NO_DATA_AVAILABLE_FOR_DATE, None, {})

        if msg.intent.calculation_type in [CalculationType.MAXIMUM, CalculationType.MINIMUM]:
            sort_order = asc if msg.intent.calculation_type == CalculationType.MINIMUM else desc
            # We only support querying the location for daily values, e.g. asking "Which country had the most
            # performed vaccinations last week" won't work, since we have to calculate the sum manually.
            if msg.slots.date is None or msg.slots.date.type == "DAY":
                query = self.session.query(table).where(and_(*time_condition, *location_condition)).order_by(
                    sort_order(considered_column)).limit(1)
                result = query.all()

                if len(result) == 0:
                    return QueryResult(msg, QueryResultCode.UNEXPECTED_RESULT, None, {})
                else:
                    return QueryResult(msg, QueryResultCode.SUCCESS, result[0].location, {})
            else:
                return QueryResult(msg, QueryResultCode.NO_MAX_MIN_FOR_COUNTRY_SUPPORTED, None, {})
        else:
            return QueryResult(msg, QueryResultCode.UNSUPPORTED_ACTION, None, {})

    def _query_date(self, table: Union[Case, Vaccination], considered_column: InstrumentedAttribute,
                    msg: Message) -> QueryResult:
        """Performs the query given that we are trying to query a date."""
        location_condition: List[bool] = self._get_location_from_condition(table, msg)

        if self.session.query(func.count(table.id)).where(and_(*location_condition)).scalar() == 0:
            return QueryResult(msg, QueryResultCode.NOT_EXISTING_LOCATION, None, {"location": msg.slots.location})

        # In theory we could also RAW_VALUE for queries like "When did Austria have 50.000 cases", but this would
        # probably require a lot of additional program logic, so for now only maximum and minimum is supported.
        if msg.intent.calculation_type in [CalculationType.MAXIMUM, CalculationType.MINIMUM]:
            sort_order = asc if msg.intent.calculation_type == CalculationType.MINIMUM else desc
            query = self.session.query(table).where(and_(*location_condition)).order_by(
                sort_order(considered_column)).limit(1)
            result = query.all()

            if len(result) == 0:
                return QueryResult(msg, QueryResultCode.UNEXPECTED_RESULT, None, {})
            else:
                return QueryResult(msg, QueryResultCode.SUCCESS, Date("DAY", result[0].date, ""), {"location": result[0].location})
        else:
            return QueryResult(msg, QueryResultCode.UNSUPPORTED_ACTION, None, {})

    def _handle_no_data_available_for_date(self, table: Union[Case, Vaccination], msg: Message,
                                           location_condition: List[bool], considered_column: InstrumentedAttribute)\
            -> QueryResult:
        last_date = self.session.query(table).where(and_(*location_condition + [not_(considered_column == None)])) \
            .order_by(desc(table.date)).limit(1).all()
        return QueryResult(msg, QueryResultCode.NO_DATA_AVAILABLE_FOR_DATE,
                           None, {"latest": Date("DAY", last_date[0].date, ""), "location": last_date[0].location})

    def _query_number(self, table: Union[Case, Vaccination], considered_column: InstrumentedAttribute,
                      msg: Message) -> QueryResult:
        """Performs the query given that we are trying to query a number."""
        # If no timeframe is given, we assume that the user is asking for today
        time_condition: List[bool] = self._get_timeframe_from_condition(table, msg)
        location_condition: List[bool] = self._get_location_from_condition(table, msg)

        if self.session.query(func.count(table.id)).where(and_(*location_condition)).scalar() == 0:
            return QueryResult(msg, QueryResultCode.NOT_EXISTING_LOCATION, None, {"location": msg.slots.location})

        if self.session.query(func.count(table.id)).where(and_(*location_condition, *time_condition)).scalar() == 0:
            # We fetch the most recent date, since many queries were asking about "today" or "yesterday", but this
            # data often is not available.
            # Also note the condition needs to be "== None" instead of "is None", otherwise it will be interpreted
            # incorrectly
            return self._handle_no_data_available_for_date(table, msg, location_condition, considered_column)

        def get_query(query_list: list):
            return self.session.query(*query_list).where(and_(
                *time_condition, *location_condition
            ))

        if msg.intent.calculation_type == CalculationType.RAW_VALUE:
            query = get_query([considered_column, table.location]).order_by(desc(table.date))
        elif msg.intent.calculation_type == CalculationType.SUM:
            query = get_query([functions.sum(considered_column), table.location]).group_by(table.location)
        elif msg.intent.calculation_type == CalculationType.MAXIMUM:
            query = get_query([functions.max(considered_column), table.location]).group_by(table.location)
        elif msg.intent.calculation_type == CalculationType.MINIMUM:
            query = get_query([functions.min(considered_column), table.location]).group_by(table.location)
        else:
            return QueryResult(msg, QueryResultCode.UNSUPPORTED_ACTION, None, {})

        if msg.intent.calculation_type == CalculationType.RAW_VALUE:
            query = query.limit(1)

        result = query.all()

        if len(result) > 1:
            return QueryResult(msg, QueryResultCode.UNEXPECTED_RESULT, None, {})
        else:
            if result[0][0] is None:
                return self._handle_no_data_available_for_date(table, msg, location_condition, considered_column)
            else:
                return QueryResult(msg, QueryResultCode.SUCCESS, result[0][0], {"location": result[0][1]})

    def _get_location_from_condition(self, table: Union[Case, Vaccination], msg: Message) -> List[bool]:
        """Extracts the condition for the location slot."""
        # If we are querying the location, we just ignore whatever is in there since we don't need it.
        # But we have to make sure that we don't get any continents or data on the whole world.
        # e.g. When asking "Where have most cases been recorded?" we don't want it to return the whole
        # world as a location. This is why we need to return the condition that excludes this locations.
        if msg.intent.value_type == ValueType.LOCATION:
            return [not_(table.location_normalized.in_(list(Location.get_continents().union(Location.get_world()))))]

        if msg.slots.location is None:
            # If we are asking for the day, we don't need the location, so we can just return an empty list.
            # But same as above, we only want to consider countries. For example for "When have most cases been reported",
            # we don't want this to return results for the whole world, but instead the country with the most cases on that
            # certain date.
            if msg.intent.value_type == ValueType.DAY:
                return [not_(table.location_normalized.in_(list(Location.get_continents().union(Location.get_world()))))]
            # If we are searching for the number, we default to searching for data on the whole world.
            else:
                return [table.location_normalized.in_(list(Location.get_world()))]
        else:
            # Otherwise, we limit the country.
            return [table.location_normalized == msg.slots.location]

    def _get_timeframe_from_condition(self, table: Union[Case, Vaccination], msg: Message) -> List[bool]:
        """Extracts the time frame for the date slot."""
        # If we are asking for the day, we just ignore any timeframes found, since the task of the query
        # is to find the date.
        if msg.intent.value_type == ValueType.DAY:
            return []
        if msg.slots.date is None:
            # If we are looking for the cumulative value, we assume by default that we are looking for the value
            # from today. However, this is already taken into account by the fact that we sort the entries descending
            # by date, so we don't need any special condition for that.
            return []

        date_type: str = msg.slots.date.type
        date_value: datetime.date = msg.slots.date.value

        # Generate the timeframe depending on what kind of time period we are dealing with.
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
        """Checks the validity of the message."""
        msg_validation: MessageValidationCode = Message.validate_message(msg)

        if msg_validation != MessageValidationCode.VALID:
            return QueryResult(msg, QueryResultCode.INVALID_MESSAGE, None, {"message_validation_code": msg_validation})

        if msg.slots.date and msg.slots.date.value > self.today:
            return QueryResult(msg, QueryResultCode.FUTURE_DATA_REQUESTED, None, {})
        return None