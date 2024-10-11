from PyQt5.QtWidgets import QApplication, QLineEdit
from database.xml_to_db import get_db_connection
from database.sql_statements import select_from_location


def populate_location_table_fields(communication_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    location_type = 'sourceLocation'

    result = select_from_location(cursor, communication_id, location_type)

    if result:
        (id, communication_id, location, location_id, use_local_filename,
         use_path_from_config, target_must_be_archived, target_history_days,
         rename_existing_file, userid, password, description, location_type) = result

        set_input_value("source_input", location)
        set_input_value("userid_source_input", userid)
        set_input_value("password_source_input", password)

    conn.close()


def set_input_value(widget_name, value):
    widget = next((widget for widget in QApplication.allWidgets() if
                   isinstance(widget, QLineEdit) and widget.objectName() == widget_name), None)
    if widget:
        widget.blockSignals(True)
        widget.setText(value or "")
        widget.blockSignals(False)

# def save_location_data (communication_id): # TODO: Implement the following function
#     conn = get_db_connection()
#     cursor = conn.cursor()
#
#     location_row = {
#         'location': get_input_value("source_input"),
#         'userid': get_input_value("userid_source_input"),
#         'password': get_input_value("password_source_input")
#     }
#
#     conn.close()


