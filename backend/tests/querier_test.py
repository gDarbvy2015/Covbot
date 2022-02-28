import json
import pathlib
from datetime import datetime, timedelta

import pytest
from spacy.tokens import Span
from sqlalchemy.orm import Session

from lib.database.database_manager import DatabaseManager
from lib.database.entities import Vaccination, Case
from lib.database.querier import Querier, QueryResult, QueryResultCode
from lib.nlu.intent.calculation_type import CalculationType
from lib.nlu.intent.intent import Intent
from lib.nlu.intent.measurement_type import MeasurementType
from lib.nlu.intent.value_domain import ValueDomain
from lib.nlu.intent.value_type import ValueType
from lib.nlu.message import Message, MessageBuilder
from lib.nlu.slot.date import Date
from lib.nlu.slot.slots import Slots
from lib.nlu.topic.topic import Topic
from lib.spacy_components.custom_spacy import get_spacy

current_day = datetime.now().date()


@pytest.fixture(scope="session")
def db_manager(request):
    db_manager = DatabaseManager("covbot_test")
    db_manager.create_database()
    db_manager.create_tables()

    yield db_manager

    db_manager.drop_tables()


@pytest.fixture(scope="session")
def session(db_manager: DatabaseManager):
    session = Session(db_manager.engine)
    add_cases(session)

    yield session

    session.rollback()


def add_cases(session):
    cases = [
        Case(id=1, date=current_day - timedelta(days=9), country="Austria", country_normalized="austria", cases=15_000,
             cumulative_cases=15_000),
        Case(id=2, date=current_day - timedelta(days=8), country="Austria", country_normalized="austria", cases=16_345,
             cumulative_cases=31_345),
        Case(id=3, date=current_day - timedelta(days=7), country="Austria", country_normalized="austria", cases=8_450,
             cumulative_cases=39_795),
        Case(id=4, date=current_day - timedelta(days=6), country="Austria", country_normalized="austria", cases=4_560,
             cumulative_cases=40_251),
        Case(id=5, date=current_day - timedelta(days=5), country="Austria", country_normalized="austria", cases=7_054,
             cumulative_cases=45_060),
        Case(id=6, date=current_day - timedelta(days=4), country="Austria", country_normalized="austria", cases=10_450,
             cumulative_cases=61_859),
        Case(id=7, date=current_day - timedelta(days=2), country="Austria", country_normalized="austria", cases=15_392,
             cumulative_cases=77_251),
        Case(id=8, date=current_day - timedelta(days=1), country="Austria", country_normalized="austria", cases=19_509,
             cumulative_cases=96_760),
        Case(id=9, date=current_day, country="Austria", country_normalized="austria", cases=12_000,
             cumulative_cases=108_760),
    ]
    session.add_all(cases)


@pytest.fixture(scope="session")
def querier(db_manager, session):
    return Querier("covbot_test", db_manager, session)


def test_check_new_cases_today_in_austria_returns_number_of_cases(querier):
    topic: Topic = Topic.CASES
    intent: Intent = Intent(CalculationType.RAW_VALUE, ValueType.NUMBER, ValueDomain.POSITIVE_CASES,
                            MeasurementType.DAILY)
    slots: Slots = Slots(Date("DAY", current_day, "today"), "austria")
    msg: Message = Message(topic, intent, slots)

    qr: QueryResult = querier.query_intent(msg)

    assert qr.result_code == QueryResultCode.SUCCESS
    assert qr.result == 12_000


def test_check_new_cases_cumulative_in_austria_returns_number_of_cases(querier):
    topic: Topic = Topic.CASES
    intent: Intent = Intent(CalculationType.RAW_VALUE, ValueType.NUMBER, ValueDomain.POSITIVE_CASES,
                            MeasurementType.CUMULATIVE)
    slots: Slots = Slots(None, "austria")
    msg: Message = Message(topic, intent, slots)

    qr: QueryResult = querier.query_intent(msg)

    assert qr.result_code == QueryResultCode.SUCCESS
    assert qr.result == 108_760


def test_check_future_date_returns_error(querier):
    topic: Topic = Topic.CASES
    intent: Intent = Intent(CalculationType.RAW_VALUE, ValueType.NUMBER, ValueDomain.POSITIVE_CASES,
                            MeasurementType.DAILY)
    slots: Slots = Slots(Date("DAY", current_day + timedelta(days=1), "today"), "austria")
    msg: Message = Message(topic, intent, slots)

    qr: QueryResult = querier.query_intent(msg)
    assert qr.result_code == QueryResultCode.FUTURE_DATA_REQUESTED


def test_check_not_existing_location_returns_error(querier):
    topic: Topic = Topic.CASES
    intent: Intent = Intent(CalculationType.RAW_VALUE, ValueType.NUMBER, ValueDomain.POSITIVE_CASES,
                            MeasurementType.DAILY)
    slots: Slots = Slots(Date("DAY", current_day, "today"), "limbo")
    msg: Message = Message(topic, intent, slots)

    qr: QueryResult = querier.query_intent(msg)
    assert qr.result_code == QueryResultCode.NOT_EXISTING_LOCATION


with open(pathlib.Path(__file__).parent / "annotated_queries.json") as query_file:
    queries = json.load(query_file)

spacy = get_spacy()
message_builder = MessageBuilder()


@pytest.mark.parametrize("query", queries)
def test_all_annotated_queries_run_without_error(querier, query):
    sent: Span = list(spacy(query["query"]).sents)[0]
    msg = message_builder.create_message(sent)
    querier.query_intent(msg)

