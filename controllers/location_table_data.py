import logging
from common.connection_manager import ConnectionManager
from .communication_table_data import set_input_value, get_input_value, set_checkbox_value, get_checkbox_value
from database.utils import select_from_location, update_location


def populate_location_table_fields(communication_id, location_type = 'sourceLocation'):
    conn_manager = ConnectionManager().get_instance()
    conn = conn_manager.get_db_connection()
    cursor = conn.cursor()

    result = select_from_location(cursor, communication_id, location_type)

    if result:
        (id, communication_id, location, location_id, use_local_filename,
         use_path_from_config, target_must_be_archived, target_history_days,
         rename_existing_file, userid, password, description, location_type) = result

        set_input_value("source_input", location)
        set_input_value("userid_source_input", userid)
        set_input_value("password_source_input", password)
        set_input_value("description_source_input", description)
        set_input_value("location_id_input", location_id)
        # set_checkbox_value("use_local_filename_checkbox", use_local_filename) TODO: Implement this
        # set_checkbox_value("use_path_from_config_checkbox", use_path_from_config)
        # set_checkbox_value("target_history_days_checkbox", target_history_days)
        # set_checkbox_value("rename_existing_file_checkbox", rename_existing_file)
        # set_checkbox_value("target_must_be_archived_checkbox", target_must_be_archived)

    conn.close()


# def save_location_data(communication_id, location_type='sourceLocation'): TODO: Implement this
#     conn_manager = ConnectionManager().get_instance()
#     conn = conn_manager.get_db_connection()
#     cursor = conn.cursor()
#
#     location_row = {
#         'location_id': get_input_value("location_id_input"),
#         'location': get_input_value("source_input"),
#         'userid': get_input_value("userid_source_input"),
#         'password': get_input_value("password_source_input"),
#         'useLocalFilename': '',
#         'usePathFromConfig': '',
#         'targetMustBeArchived': '',
#         'targetHistoryDays': '',
#         'renameExistingFile': '',
#         'description': get_input_value("description_source_input"),
#         'locationType': location_type,
#         'communication_id': communication_id,
#     }
#
#     logging.info(f"Saving location data for communication_id {communication_id}:")
#     logging.info(location_row)
#
#     try:
#         update_location(cursor, location_row)
#         conn.commit()
#         logging.info("Data saved successfully.")
#     except Exception as e:
#         logging.error(f"Error while saving data: {e}")
#     finally:
#         conn.close()
