from controllers.utils.get_db_connection import get_db_connection
from database.utils import update_location, select_from_location
from controllers.utils.get_and_set_value import (get_input_value, set_input_value, get_checkbox_value,
                                                 set_checkbox_value, convert_checkbox_to_string)



#Populating function
def populate_location_source_fields(communication_id, location_type='sourceLocation'):
    conn, cursor = get_db_connection()

    result = select_from_location(cursor, communication_id, location_type).fetchone()

    if result:
        populate_source_fields(result)

    conn.close()


def populate_source_fields(result):
    (id, communication_id, location, location_id, use_local_filename,
     use_path_from_config, target_must_be_archived, target_history_days,
     rename_existing_file, userid, password, description, location_type) = result

    set_input_value("source_input", location)
    set_input_value("userid_source_input", userid)
    set_input_value("password_source_input", password)
    set_input_value("description_source_input", description)
    set_input_value("location_id_input", location_id)
    set_checkbox_value("use_local_filename_checkbox", use_local_filename)
    set_checkbox_value("use_path_from_config_checkbox", use_path_from_config)
    set_checkbox_value("target_history_days_checkbox", target_history_days)
    set_checkbox_value("rename_existing_file_checkbox", rename_existing_file)
    set_checkbox_value("target_must_be_archived_checkbox", target_must_be_archived)


#Save function
def save_location_data(communication_id, location_type='sourceLocation'):
    conn, cursor = get_db_connection()

    location_row = create_location_row(communication_id, location_type)

    update_location(cursor, location_row)
    conn.commit()
    conn.close()


def create_location_row(communication_id, location_type):
    return {
        'location_id': get_input_value("location_id_input"),
        'location': get_input_value("source_input"),
        'userid': get_input_value("userid_source_input"),
        'password': get_input_value("password_source_input"),
        'useLocalFilename': convert_checkbox_to_string(get_checkbox_value("use_local_filename_checkbox")),
        'usePathFromConfig': convert_checkbox_to_string(get_checkbox_value("use_path_from_config_checkbox")),
        'targetMustBeArchived': convert_checkbox_to_string(get_checkbox_value("target_must_be_archived_checkbox")),
        'targetHistoryDays': convert_checkbox_to_string(get_checkbox_value("target_history_days_checkbox")),
        'renameExistingFile': convert_checkbox_to_string(get_checkbox_value("rename_existing_file_checkbox")),
        'description': get_input_value("description_source_input"),
        'locationType': location_type,
        'communication_id': communication_id,
    }

def populate_location_target_fields(communication_id, location_type='targetLocation'):
    conn, cursor = get_db_connection()

    result = select_from_location(cursor, communication_id, location_type)

    if result:
        populate_target_fields(result)

    conn.close()

def populate_target_fields(result):
    (id, communication_id, location, location_id, use_local_filename,
     use_path_from_config, target_must_be_archived, target_history_days,
     rename_existing_file, userid, password, description, location_type) = result

    set_input_value("target_second_input", location)
    set_input_value("userid_target_second_input", userid)
    set_input_value("password_target_second_input", password)
    set_input_value("description_target_second_input", description)
    set_input_value("location_id_target_second_input", location_id)
    set_checkbox_value("use_local_filename_checkbox_target_second", use_local_filename)
    set_checkbox_value("use_path_from_config_checkbox_target_second", use_path_from_config)
    set_checkbox_value("target_history_days_checkbox_second", target_history_days)
    set_checkbox_value("rename_existing_file_checkbox_second", rename_existing_file)
    set_checkbox_value("target_must_be_archived_checkbox_second", target_must_be_archived)