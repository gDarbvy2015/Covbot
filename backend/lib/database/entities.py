from __future__ import annotations
import pandas
from sqlalchemy import Column, Integer, String, Date, BigInteger
from sqlalchemy.orm import declarative_base
from sqlalchemy.engine.base import Engine

# declarative base class
Base = declarative_base()


class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    country = Column(String(256))
    country_normalized = Column(String(256))
    cases = Column(BigInteger)
    cumulative_cases = Column(BigInteger)


class Vaccination(Base):
    __tablename__ = "vaccinations"

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    country = Column(String(256))
    country_normalized = Column(String(256))
    total_vaccinations = Column(BigInteger)
    people_vaccinated = Column(BigInteger)
    daily_vaccinations = Column(Integer)
    daily_people_vaccinated = Column(Integer)


def create_tables(engine: Engine) -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

