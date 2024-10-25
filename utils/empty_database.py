import sqlite3
from common.connection_manager import ConnectionManager
from database.utils import select_all_tablenames_from_db


def empty_database():
    conn_manager = ConnectionManager().get_instance()
    conn = conn_manager.get_db_connection()
    cursor = conn.cursor()

    try:
        select_all_tablenames_from_db(cursor)
        tables = cursor.fetchall()

        for table in tables:
            table_name = table[0]
            cursor.execute(f"DELETE FROM {table_name};")
            print(f"Deleted all data from table: {table_name}")

        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()
