import os

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine


class DatabaseConnection:
    """Class that represents a connection to the database for Covbot."""
    def __init__(self):
        self._host: str = os.environ.get("COVBOT_DB_HOST")
        self._port: str = os.environ.get("COVBOT_DB_PORT")
        self._user: str = os.environ.get("COVBOT_USER")
        self._password: str = os.environ.get("COVBOT_PASSWORD")
        self._db_server_link: str = f"mysql://{self._user}:{self._password}@{self._host}:{self._port}/"

    def create_engine(self, db_name: str = None) -> Engine:
        """Creates an engine pointing to the database for Covbot."""
        if not db_name:
            return create_engine(self._db_server_link)
        else:
            return create_engine(self._db_server_link + db_name)
