from typing import Tuple, Any, Union, List

from lib.database.database_connection import DatabaseConnection
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.sql.selectable import Select
from lib.database.entities import Case, Vaccination


class Querier:
    def __init__(self):
        self.engine = DatabaseConnection().create_engine("covbot")
        self.session = Session(self.engine, future=True)



if __name__ == '__main__':
    pass
