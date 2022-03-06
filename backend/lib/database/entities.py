from __future__ import annotations

from sqlalchemy import Column, Integer, String, Date, BigInteger
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import declarative_base

# declarative base class
Base = declarative_base()


class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    location = Column(String(256))
    location_normalized = Column(String(256))
    cases = Column(BigInteger)
    cumulative_cases = Column(BigInteger)

    def __repr__(self):
        return f"Case(id={self.id}, date={self.date}, location={self.location}, " \
               f"location_normalized={self.location_normalized}, cases={self.cases}, " \
               f"cumulative_cases={self.cumulative_cases})"


class Vaccination(Base):
    __tablename__ = "vaccinations"

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    location = Column(String(256))
    location_normalized = Column(String(256))
    total_vaccinations = Column(BigInteger)
    people_vaccinated = Column(BigInteger)
    daily_vaccinations = Column(Integer)
    daily_people_vaccinated = Column(Integer)

    def __repr__(self):
        return f"Case(id={self.id}, date={self.date}, location={self.location}, " \
               f"location_normalized={self.location_normalized}, total_vaccinations={self.total_vaccinations}, " \
               f"people_vaccinated={self.people_vaccinated}, daily_vaccinations={self.daily_vaccinations}, " \
               f"daily_people_vaccinated={self.daily_people_vaccinated})"


def create_tables(engine: Engine, tables=None) -> None:
    if tables is None:
        tables = [Vaccination.__table__, Case.__table__]
    drop_tables(engine, tables)
    Base.metadata.create_all(engine, tables)


def drop_tables(engine: Engine, tables=None) -> None:
    if tables is None:
        tables = [Vaccination.__table__, Case.__table__]
    Base.metadata.drop_all(engine, tables)
