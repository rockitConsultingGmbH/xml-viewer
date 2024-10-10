import os
import sqlite3

class ConnectionManager:
    def __init__(self, db_path):
        self.db_path = db_path

    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), 'database.db')

    def get_db_connection(self):
        try:
            connection = sqlite3.connect(self.db_path)
            connection.row_factory = sqlite3.Row
            return connection
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None