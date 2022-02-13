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
    positive_cases = Column(BigInteger)
    cumulative_positive_cases = Column(BigInteger)

    @staticmethod
    def from_pandas_row(row: pandas.Series) -> Case:
        return Case(
            country=row["country"],
            date=row["date"],
            positive_cases=row["cases"],
            country_normalized=row["country_normalized"],
            cumulative_positive_cases=row["cumulative_cases"]
        )


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
    Base.metadata.create_all(engine)

