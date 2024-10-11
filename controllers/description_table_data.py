from common.connection_manager import ConnectionManager
from database.utils import select_from_description
from .communication_table_data import set_input_value, get_input_value

def populate_description_fields(communication_id):
    conn_manager = ConnectionManager().get_instance()
    conn = conn_manager.get_db_connection()
    cursor = conn.cursor()

    description_types = ['description', 'description1', 'description2', 'description3']
    input_names = ["description_input", "description_1_input", "description_2_input", "description_3_input"]

    for desc_type, input_name in zip(description_types, input_names):
        result = select_from_description(cursor, communication_id, desc_type)
        if result:
            _, _, description_text, _ = result
            set_input_value(input_name, description_text)

    conn.close()

set_input_value("widget_name", "value")
get_input_value("widget_name")