""" Setup script

This script will download any additional necessary dependencies and set up the database to run the other
parts of the chatbot.

"""
from lib.database.database_manager import DatabaseManager

if __name__ == '__main__':
    database_manager = DatabaseManager()
    database_manager.create_database()
    database_manager.update_database()

    database_manager = DatabaseManager("covbot_test")
    database_manager.create_database()
