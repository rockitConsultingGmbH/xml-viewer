import os
import sqlite3

class ConnectionManager:
    _instance = None

    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'database.db')

    @classmethod
    def get_instance(cls):
        """Method to retrieve the singleton instance of ConnectionManager."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_db_connection(self):
        """Method to create and return a database connection."""
        try:
            # Create a new SQLite connection
            connection = sqlite3.connect(self.db_path)
            connection.row_factory = sqlite3.Row  # To return rows as dictionaries
            return connection
        except sqlite3.Error as e:
            print(f"An error occurred while connecting to the database: {e}")
            return None
