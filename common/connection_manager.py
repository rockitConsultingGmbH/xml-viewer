import logging
import os
import sqlite3

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class ConnectionManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ConnectionManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'database.db')
            self.initialized = True

    def get_db_connection(self):
        try:
            connection = sqlite3.connect(self.db_path)
            connection.row_factory = sqlite3.Row
            return connection
        except sqlite3.Error as e:
            logging.debug(f"An error occurred while connecting to the database: {e}")
            return None
