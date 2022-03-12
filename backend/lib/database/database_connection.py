import os
import pathlib

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine


class DatabaseConnection:
    """Class that represents a connection to the database for Covbot."""
    def __init__(self):
        self._db_server_link: str = "sqlite:///" + os.environ.get("COVBOT_DB_PATH")

    def create_engine(self, db_name: str = "covbot") -> Engine:
        """Creates an engine pointing to the database for Covbot."""
        return create_engine(str(self._db_server_link) + db_name + ".db")
