import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.exc import DatabaseError
import logging


logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


def create_database() -> None:
    logger.info("Creating the database for Covbot...")
    host = os.environ.get("COVBOT_DB_HOST")
    port = os.environ.get("COVBOT_DB_PORT")
    user = os.environ.get("COVBOT_USER")
    password = os.environ.get("COVBOT_PASSWORD")
    engine = create_engine(f"mysql://{user}:{password}@{host}:{port}")

    try:
        engine.execute("CREATE DATABASE covbot")
        logger.info("Database was created successfully.")
    except DatabaseError as e:
        if "1007" in str(e):
            logger.info("Couldn't create the database because it already exists.")
        else:
            logger.error("Unexpected error occurred while creating the database for Covbot: ", str(e))
            return

    create_tables()


def create_tables() -> None:
    pass


if __name__ == '__main__':
    create_database()