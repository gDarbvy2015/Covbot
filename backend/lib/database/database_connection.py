import os
from sqlalchemy.engine.base import Engine
from sqlalchemy import create_engine


class DatabaseConnection:
    def __init__(self):
        self._host = os.environ.get("COVBOT_DB_HOST")
        self._port = os.environ.get("COVBOT_DB_PORT")
        self._user = os.environ.get("COVBOT_USER")
        self._password = os.environ.get("COVBOT_PASSWORD")
        self._db_server_link = f"mysql://{self._user}:{self._password}@{self._host}:{self._port}/"

    def create_engine(self, db_name: str = None) -> Engine:
        if not db_name:
            return create_engine(self._db_server_link)
        else:
            return create_engine(self._db_server_link + db_name)