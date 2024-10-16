from common.connection_manager import ConnectionManager

def get_db_connection():
    conn_manager = ConnectionManager().get_instance()
    conn = conn_manager.get_db_connection()
    cursor = conn.cursor()
    return conn, cursor