from common.connection_manager import ConnectionManager
from database.utils import update_location, select_from_location
from controllers.utils.get_and_set_value import (get_input_value, set_input_value,
                                                 get_checkbox_value, set_checkbox_value,
                                                 convert_checkbox_to_string)


def populate_location_source_fields(communication_id, location_type='sourceLocation'):
    conn_manager = ConnectionManager().get_instance()
    conn = conn_manager.get_db_connection()
    cursor = conn.cursor()
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
    set_input_value("source_description_input", description)
    set_input_value("location_id_input", location_id)
    set_checkbox_value("use_local_filename_checkbox", use_local_filename)
    set_checkbox_value("use_path_from_config_checkbox", use_path_from_config)
    set_checkbox_value("target_history_days_checkbox", target_history_days)
    set_checkbox_value("rename_existing_file_checkbox", rename_existing_file)
    set_checkbox_value("target_must_be_archived_checkbox", target_must_be_archived)


def save_source_location_data(communication_id, location_type='sourceLocation'):
    conn_manager = ConnectionManager().get_instance()
    conn = conn_manager.get_db_connection()
    cursor = conn.cursor()
    source_location = cursor.fetchone()
    if source_location:
        location_row = create_source_location_row(source_location, communication_id, location_type)
        update_location(cursor, location_row)
        conn.commit()
    conn.close()


def create_source_location_row(source_location, communication_id, location_type):
    return {
        'id': source_location[0],
        'location_id': get_input_value("location_id_input"),
        'location': get_input_value("source_input"),
        'userid': get_input_value("userid_source_input"),
        'password': get_input_value("password_source_input"),
        'useLocalFilename': convert_checkbox_to_string(get_checkbox_value("use_local_filename_checkbox")),
        'usePathFromConfig': convert_checkbox_to_string(get_checkbox_value("use_path_from_config_checkbox")),
        'targetMustBeArchived': convert_checkbox_to_string(get_checkbox_value("target_must_be_archived_checkbox")),
        'targetHistoryDays': convert_checkbox_to_string(get_checkbox_value("target_history_days_checkbox")),
        'renameExistingFile': convert_checkbox_to_string(get_checkbox_value("rename_existing_file_checkbox")),
        'description': get_input_value("source_description_input"),
        'locationType': location_type,
        'communication_id': communication_id,
    }


def populate_location_target_fields(communication_id, location_type='targetLocation'):
    conn_manager = ConnectionManager().get_instance()
    conn = conn_manager.get_db_connection()
    cursor = conn.cursor()
    targetLocations = select_from_location(cursor, communication_id, location_type).fetchall()
    for targetLocation in targetLocations:
        if targetLocation:
            populate_target_fields(targetLocation)
    conn.close()


def populate_target_fields(targetLocation):
    set_input_value(f"target_{targetLocation['id']}_input", targetLocation["location"])
    set_input_value(f"userid_target_{targetLocation['id']}_input", targetLocation["userid"])
    set_input_value(f"password_target_{targetLocation['id']}_input", targetLocation["password"])
    set_input_value(f"target_description_{targetLocation['id']}_input", targetLocation["description"])
    set_input_value(f"location_id_target_{targetLocation['id']}_input", targetLocation["location_id"])
    set_checkbox_value(f"use_local_filename_checkbox_target_{targetLocation['id']}", targetLocation["useLocalFilename"])
    set_checkbox_value(f"use_path_from_config_checkbox_target_{targetLocation['id']}",
                       targetLocation["usePathFromConfig"])
    set_checkbox_value(f"target_history_days_checkbox_{targetLocation['id']}", targetLocation["targetHistoryDays"])
    set_checkbox_value(f"rename_existing_file_checkbox_{targetLocation['id']}", targetLocation["renameExistingFile"])
    set_checkbox_value(f"target_must_be_archived_checkbox_{targetLocation['id']}",
                       targetLocation["targetMustBeArchived"])


def save_target_location_data(communication_id, location_type='targetLocation'):
    conn_manager = ConnectionManager().get_instance()
    conn = conn_manager.get_db_connection()
    cursor = conn.cursor()
    cursor = select_from_location(cursor, communication_id, location_type)
    target_locations = cursor.fetchall()
    if target_locations:
        for target_location in target_locations:
            location_row = create_target_location_row(target_location, communication_id, location_type)
            update_location(cursor, location_row)
        conn.commit()
    conn.close()


def create_target_location_row(target_location, communication_id, location_type):
    return {
        'id': target_location[0],
        'location_id': get_input_value(f"location_id_target_{target_location[0]}_input"),
        'location': get_input_value(f"target_{target_location[0]}_input"),
        'userid': get_input_value(f"userid_target_{target_location[0]}_input"),
        'password': get_input_value(f"password_target_{target_location[0]}_input"),
        'useLocalFilename': convert_checkbox_to_string(
            get_checkbox_value(f"use_local_filename_checkbox_target_{target_location[0]}")),
        'usePathFromConfig': convert_checkbox_to_string(
            get_checkbox_value(f"use_path_from_config_checkbox_target_{target_location[0]}")),
        'targetMustBeArchived': convert_checkbox_to_string(
            get_checkbox_value(f"target_must_be_archived_checkbox_{target_location[0]}")),
        'targetHistoryDays': convert_checkbox_to_string(
            get_checkbox_value(f"target_history_days_checkbox_{target_location[0]}")),
        'renameExistingFile': convert_checkbox_to_string(
            get_checkbox_value(f"rename_existing_file_checkbox_{target_location[0]}")),
        'description': get_input_value(f"target_description_{target_location[0]}_input"),
        'locationType': location_type,
        'communication_id': communication_id,
    }
