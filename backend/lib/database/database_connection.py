import os
import pathlib

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine


class DatabaseConnection:
    """Class that represents a connection to the database for Covbot."""
    def __init__(self):
        self._db_path: pathlib.Path = pathlib.Path(os.environ.get("COVBOT_DB_PATH"))

    def create_engine(self, db_name: str = "covbot") -> Engine:
        """Creates an engine pointing to the database for Covbot."""
        return create_engine("sqlite:///" + str(self._db_path / (db_name + ".db")))
