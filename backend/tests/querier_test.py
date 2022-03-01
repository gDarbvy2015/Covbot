import json
import pathlib
from datetime import datetime, timedelta
from typing import Optional

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

# If this is changed, most test cases will need to be changed
current_day = datetime(2022, 2, 24).date()


@pytest.fixture(scope="session")
def db_manager():
    db_manager = DatabaseManager("covbot_test")
    db_manager.create_database()
    db_manager.create_tables()

    yield db_manager

    db_manager.drop_tables()


@pytest.fixture(autouse=True)
def session(db_manager: DatabaseManager):
    session = Session(db_manager.engine)
    yield session
    session.rollback()


def add_austria_cases(session):
    cases = [
        Case(id=1, date=current_day - timedelta(days=9), country="Austria", country_normalized="austria", cases=15000,
             cumulative_cases=15000),
        Case(id=2, date=current_day - timedelta(days=8), country="Austria", country_normalized="austria", cases=16345,
             cumulative_cases=31345),
        Case(id=3, date=current_day - timedelta(days=7), country="Austria", country_normalized="austria", cases=8450,
             cumulative_cases=39795),
        Case(id=4, date=current_day - timedelta(days=6), country="Austria", country_normalized="austria", cases=4560,
             cumulative_cases=40251),
        Case(id=5, date=current_day - timedelta(days=5), country="Austria", country_normalized="austria", cases=7054,
             cumulative_cases=45060),
        Case(id=6, date=current_day - timedelta(days=4), country="Austria", country_normalized="austria", cases=10450,
             cumulative_cases=61859),
        Case(id=7, date=current_day - timedelta(days=2), country="Austria", country_normalized="austria", cases=15392,
             cumulative_cases=77251),
        Case(id=8, date=current_day - timedelta(days=1), country="Austria", country_normalized="austria", cases=19509,
             cumulative_cases=96760),
        Case(id=9, date=current_day, country="Austria", country_normalized="austria", cases=12000,
             cumulative_cases=108760),
    ]
    session.add_all(cases)


def add_austria_vaccinations(session):
    vaccinations = [
        Vaccination(id=1, date=current_day - timedelta(days=6), country="Austria", country_normalized="austria",
                    total_vaccinations=1200, people_vaccinated=1200, daily_vaccinations=1200,
                    daily_people_vaccinated=1200),
        Vaccination(id=2, date=current_day - timedelta(days=5), country="Austria", country_normalized="austria",
                    total_vaccinations=2700, people_vaccinated=2500, daily_vaccinations=1500,
                    daily_people_vaccinated=1300),
        Vaccination(id=3, date=current_day - timedelta(days=4), country="Austria", country_normalized="austria",
                    total_vaccinations=3500, people_vaccinated=3100, daily_vaccinations=800,
                    daily_people_vaccinated=600),
        Vaccination(id=4, date=current_day - timedelta(days=3), country="Austria", country_normalized="austria",
                    total_vaccinations=6900, people_vaccinated=6100, daily_vaccinations=3400,
                    daily_people_vaccinated=3000),
        Vaccination(id=5, date=current_day - timedelta(days=2), country="Austria", country_normalized="austria",
                    total_vaccinations=10500, people_vaccinated=9300, daily_vaccinations=3600,
                    daily_people_vaccinated=3200),
        Vaccination(id=6, date=current_day - timedelta(days=1), country="Austria", country_normalized="austria",
                    total_vaccinations=11000, people_vaccinated=9600, daily_vaccinations=500,
                    daily_people_vaccinated=300),
    ]
    session.add_all(vaccinations)


@pytest.fixture
def querier(db_manager, session):
    return Querier("covbot_test", db_manager, session, current_day)


def get_cases_message(topic: Topic = Topic.CASES, calculation_Type: CalculationType = CalculationType.RAW_VALUE,
                      value_type: ValueType = ValueType.NUMBER, value_domain: ValueDomain = ValueDomain.POSITIVE_CASES,
                      measurement_type: MeasurementType = MeasurementType.DAILY,
                      slot_date: Optional[Date] = Date("DAY", current_day, "today"),
                      slot_location: Optional[str] = "austria"):
    topic: Topic = topic
    intent: Intent = Intent(calculation_Type, value_type, value_domain, measurement_type)
    slots: Slots = Slots(slot_date, slot_location)
    msg: Message = Message(topic, intent, slots)

    return msg


def get_vaccinations_message(topic: Topic = Topic.VACCINATIONS, calculation_Type: CalculationType = CalculationType.RAW_VALUE,
                      value_type: ValueType = ValueType.NUMBER, value_domain: ValueDomain = ValueDomain.ADMINISTERED_VACCINES,
                      measurement_type: MeasurementType = MeasurementType.DAILY,
                      slot_date: Optional[Date] = Date("DAY", current_day, "today"),
                      slot_location: Optional[str] = "austria"):
    topic: Topic = topic
    intent: Intent = Intent(calculation_Type, value_type, value_domain, measurement_type)
    slots: Slots = Slots(slot_date, slot_location)
    msg: Message = Message(topic, intent, slots)

    return msg


def test_check_new_cases_today_in_austria_returns_number_of_cases(querier, session):
    msg: Message = get_cases_message()

    add_austria_cases(session)

    qr: QueryResult = querier.query_intent(msg)

    assert qr.result_code == QueryResultCode.SUCCESS
    assert qr.result == 12000

def test_check_new_vaccinations_yesterday_in_austria_returns_number_of_vaccinations(querier, session):
    msg: Message = get_cases_message()

    add_austria_vaccinations(session)

    qr: QueryResult = querier.query_intent(msg)

    assert qr.result_code == QueryResultCode.SUCCESS
    assert qr.result == 12000


def test_check_new_cases_this_week_in_austria_returns_number_of_cases(querier, session):
    msg: Message = get_cases_message(calculation_Type=CalculationType.SUM,
                                     slot_date=Date("WEEK", current_day, "this week"))

    add_austria_cases(session)

    qr: QueryResult = querier.query_intent(msg)

    assert qr.result_code == QueryResultCode.SUCCESS
    assert qr.result == 46901


def test_check_new_cases_cumulative_in_austria_returns_number_of_cases(querier, session):
    msg: Message = get_cases_message(measurement_type=MeasurementType.CUMULATIVE,
                                     slot_date=None)

    add_austria_cases(session)

    qr: QueryResult = querier.query_intent(msg)

    assert qr.result_code == QueryResultCode.SUCCESS
    assert qr.result == 108760


def test_check_future_date_returns_error(querier, session):
    msg: Message = get_cases_message(slot_date=Date("DAY", current_day + timedelta(days=1), "today"))

    add_austria_cases(session)

    qr: QueryResult = querier.query_intent(msg)
    assert qr.result_code == QueryResultCode.FUTURE_DATA_REQUESTED


def test_check_not_existing_location_returns_error(querier, session):
    msg: Message = get_cases_message(slot_location="limbo")

    add_austria_cases(session)

    qr: QueryResult = querier.query_intent(msg)
    assert qr.result_code == QueryResultCode.NOT_EXISTING_LOCATION


with open(pathlib.Path(__file__).parent / "annotated_queries.json") as query_file:
    queries = json.load(query_file)

spacy = get_spacy()
message_builder = MessageBuilder()


@pytest.mark.parametrize("query", queries)
@pytest.mark.skip(reason="check these queries in the end")
def test_all_annotated_queries_run_without_error(querier, query, session):
    sent: Span = list(spacy(query["query"]).sents)[0]
    msg = message_builder.create_message(sent)

    add_austria_cases(session)
    add_austria_vaccinations(session)

    querier.query_intent(msg)

