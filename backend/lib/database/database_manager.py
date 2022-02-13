from sqlalchemy.exc import DatabaseError
from lib.util.logger import Logger

from lib.database.dataset_handler import DatasetHandler
from lib.database.database_connection import DatabaseConnection
from lib.database.entities import create_tables, Vaccination, Case


class DatabaseManager:
    def __init__(self):
        self.logger = Logger(__name__)
        self.connection = DatabaseConnection()
        self.db_name = "covbot"
        self.dataset_handler = DatasetHandler()

    def create_database(self) -> None:
        self.logger.info("Creating the database for Covbot...")
        engine = self.connection.create_engine()

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

    def update_database(self) -> None:
        self.logger.info("Updating the data in the database...")
        self.update_covid_cases()
        self.update_vaccinations()

    def update_covid_cases(self) -> None:
        covid_cases = self.dataset_handler.load_covid_cases()

        engine = self.connection.create_engine(self.db_name)
        db_connection = engine.connect()

        self.logger.info("Updating the daily detected covid cases...")
        covid_cases.to_sql(name="cases", con=db_connection, if_exists="replace", index=False)
        self.logger.info("Daily detected covid cases were updated.")

    def update_vaccinations(self) -> None:
        vaccinations = self.dataset_handler.load_vaccinations()

        engine = self.connection.create_engine(self.db_name)
        db_connection = engine.connect()

        self.logger.info("Updating daily vaccinations...")
        vaccinations.to_sql(name="vaccinations", con=db_connection, if_exists="replace", index=False)
        self.logger.info("Daily vaccinations were updated.")

    def _create_tables(self) -> None:
        engine = self.connection.create_engine(self.db_name)
        create_tables(engine)


if __name__ == '__main__':
    database_creator = DatabaseManager()
    database_creator.create_database()
    database_creator.update_database()