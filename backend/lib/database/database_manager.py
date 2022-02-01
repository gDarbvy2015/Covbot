import os
import sys

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, DATE, String, BigInteger
from sqlalchemy.exc import DatabaseError
import logging

from lib.database.dataset_handler import DatasetHandler


class DatabaseManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.host = os.environ.get("COVBOT_DB_HOST")
        self.port = os.environ.get("COVBOT_DB_PORT")
        self.user = os.environ.get("COVBOT_USER")
        self.password = os.environ.get("COVBOT_PASSWORD")
        self.db_server_link = f"mysql://{self.user}:{self.password}@{self.host}:{self.port}/"
        self.db_name = "covbot"

        self.logger.addHandler(logging.StreamHandler(sys.stdout))
        self.logger.setLevel(logging.INFO)

    def create_database(self) -> None:
        self.logger.info("Creating the database for Covbot...")
        engine = create_engine(self.db_server_link)

        try:
            engine.execute(f"CREATE DATABASE {self.db_name}")
            self.logger.info("Database was created successfully.")
        except DatabaseError as e:
            if "1007" in str(e):
                self.logger.info("Couldn't create the database because it already exists.")
            else:
                self.logger.error("Unexpected error occurred while creating the database for Covbot: ", str(e))
                return

        self._create_tables()
        self.update_database()

    def update_database(self) -> None:
        self.logger.info("Updating the data in the database...")

        dataset_handler = DatasetHandler()
        covid_cases = dataset_handler.load_covid_cases()

        engine = create_engine(self.db_server_link + f"{self.db_name}")
        db_connection = engine.connect()

        cases_dtypes = {"date": DATE, "country": String(256), "cases": BigInteger}
        covid_cases.to_sql(name="cases", con=db_connection, if_exists="replace", index=False, dtype=cases_dtypes)

    def _create_tables(self) -> None:
        metadata = MetaData()
        engine = create_engine(self.db_server_link + f"{self.db_name}")

        Table(
            "cases", metadata,
            Column("id", Integer, primary_key=True),
            Column("date", DATE),
            Column("country", String(256)),
            Column("cases", BigInteger)
        )

        metadata.create_all(engine)


if __name__ == '__main__':
    database_creator = DatabaseManager()
    database_creator.create_database()