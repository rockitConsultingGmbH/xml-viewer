from common.connection_manager import ConnectionManager
from database.utils import select_from_description, update_description
from controllers.utils.get_and_set_value import set_input_value, get_input_value
from gui.communication_ui_components.descriptions import input_names


def populate_description_fields(communication_id):
    conn_manager = ConnectionManager().get_instance()
    conn = conn_manager.get_db_connection()
    cursor = conn.cursor()

    for input_name in input_names:
        description_id = input_name.split('_')[1]
        result = select_from_description(cursor, communication_id, description_id).fetchone()
        if result:
            _, _, description_text, _ = result
            set_input_value(input_name, description_text)

    conn.close()


def save_description_data(communication_id):
    conn_manager = ConnectionManager().get_instance()
    conn = conn_manager.get_db_connection()
    cursor = conn.cursor()

    for input_name in input_names:
        description_text = get_input_value(input_name)

        if description_text:
            description_id = input_name.split('_')[1]
            existing_result = select_from_description(cursor, communication_id, description_id).fetchone()

            if existing_result:
                description_row = {
                    'description_id': existing_result['id'],
                    'description': description_text,
                    'descriptionType': existing_result['descriptionType']
                }
                update_description(cursor, description_row)

    conn.commit()
    conn.close()
