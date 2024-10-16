from controllers.utils.get_db_connection import get_db_connection
from database.utils import select_from_description, insert_into_description, update_description
from controllers.utils.get_and_set_value import set_input_value, get_input_value

description_types = ['description', 'description1', 'description2', 'description3']
input_names = ["description_input", "description_1_input", "description_2_input", "description_3_input"]


def populate_description_fields(communication_id):
    conn, cursor = get_db_connection()

    for desc_type, input_name in zip(description_types, input_names):
        result = select_from_description(cursor, communication_id, desc_type).fetchone()
        if result:
            _, _, description_text, _ = result
            set_input_value(input_name, description_text)

    conn.close()

def save_description_data(communication_id):
    conn, cursor = get_db_connection()

    for desc_type, input_name in zip(description_types, input_names):
        description_text = get_input_value(input_name)

        if description_text:
            existing_result = select_from_description(cursor, communication_id, desc_type)

            if existing_result:
                description_row = {
                    'communication_id': communication_id,
                    'description': description_text,
                    'descriptionType': desc_type
                }
                update_description(cursor, description_row)
            else:
                new_description_row = {
                    'communication_id': communication_id,
                    'description': description_text,
                    'descriptionType': desc_type
                }
                insert_into_description(cursor, new_description_row)

    conn.commit()
    conn.close()
