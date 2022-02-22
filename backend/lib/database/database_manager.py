from sqlalchemy.exc import DatabaseError
from lib.util.logger import Logger

from lib.database.dataset_handler import DatasetHandler
from lib.database.database_connection import DatabaseConnection
from lib.database.entities import create_tables, Vaccination, Case, drop_tables


class DatabaseManager:
    def __init__(self, db_name="covbot"):
        self.logger = Logger(__name__)
        self.connection = DatabaseConnection()
        self.db_name = db_name
        self.engine = self.connection.create_engine(self.db_name)
        self.dataset_handler = DatasetHandler()

    def create_database(self) -> None:
        self.logger.info(f"Creating the database {self.db_name}...")

        try:
            self.engine.execute(f"CREATE DATABASE {self.db_name}")
            self.logger.info("Database was created successfully.")
        except DatabaseError as e:
            if "1007" in str(e):
                self.logger.info("Couldn't create the database because it already exists.")
            else:
                self.logger.error(f"Unexpected error occurred while creating the database for {self.db_name}: ", str(e))
                return

        self.create_tables()

    def update_database(self) -> None:
        self.logger.info("Updating the data in the database...")
        self.update_covid_cases()
        self.update_vaccinations()

    def update_covid_cases(self) -> None:
        covid_cases = self.dataset_handler.load_covid_cases()
        db_connection = self.engine.connect()

        self.logger.info("Deleting previous covid cases entries...")
        drop_tables(self.engine, [Case.__table__])
        create_tables(self.engine, [Case.__table__])
        self.logger.info("Updating the daily detected covid cases...")
        covid_cases.to_sql(name="cases", con=db_connection, if_exists="append", index=False)
        self.logger.info("Daily detected covid cases were updated.")

    def update_vaccinations(self) -> None:
        vaccinations = self.dataset_handler.load_vaccinations()
        db_connection = self.engine.connect()

        self.logger.info("Deleting previous vaccinations entries...")
        drop_tables(self.engine, [Vaccination.__table__])
        create_tables(self.engine, [Vaccination.__table__])
        self.logger.info("Updating daily vaccinations...")
        vaccinations.to_sql(name="vaccinations", con=db_connection, if_exists="append", index=False)
        self.logger.info("Daily vaccinations were updated.")

    def create_tables(self) -> None:
        create_tables(self.engine)

    def drop_tables(self) -> None:
        drop_tables(self.engine)


if __name__ == '__main__':
    database_creator = DatabaseManager()
    database_creator.create_database()
    database_creator.update_database()
