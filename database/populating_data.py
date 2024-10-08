from PyQt5.QtWidgets import QApplication, QLineEdit, QCheckBox
from database.xml_data_to_db import get_db_connection


def fetch_communication_data(cursor, name):
    cursor.execute(
        """SELECT isToPoll, description, description1, description2, description3,
                  pollUntilFound, noTransfer, befoerderungAb, befoerderungBis,
                  pollInterval, watcherEscalationTimeout, preunzip, postzip,
                  renameWithTimestamp, gueltigAb, gueltigBis, findPattern, quitPattern,
                  ackPattern, zipPattern, movPattern, putPattern, rcvPattern
           FROM Communication WHERE name = ?""",
        (name,)
    )
    return cursor.fetchone()


def fetch_source_locations(cursor, name):
    cursor.execute(
        "SELECT location, userid, password FROM Location WHERE communication_id = (SELECT id FROM Communication WHERE name = ?) AND locationType = 'sourceLocation'",
        (name,)
    )
    return cursor.fetchall()


def fetch_target_locations(cursor, name):
    cursor.execute(
        "SELECT location, userid, password FROM Location WHERE communication_id = (SELECT id FROM Communication WHERE name = ?) AND locationType = 'targetLocation'",
        (name,)
    )
    return cursor.fetchall()


def fetch_alternate_name_list(cursor, name):
    cursor.execute(
        "SELECT alternateName FROM AlternateNameList WHERE communication_id = (SELECT id FROM Communication WHERE name = ?)",
        (name,)
    )
    alternate_name_list_result = cursor.fetchall()

    alternate_name_list_input = next((widget for widget in QApplication.allWidgets() if
                                      isinstance(widget, QLineEdit) and widget.objectName() == "alternate_name_list_input"),
                                     None)
    if alternate_name_list_input:
        alternate_name_list_input.blockSignals(True)
        alternate_name_list_input.setText(", ".join(item[0] for item in alternate_name_list_result))
        alternate_name_list_input.blockSignals(False)


def update_widget_text(widget, text):
    if widget:
        widget.blockSignals(True)
        widget.setText(text)
        widget.blockSignals(False)


def update_checkbox_state(widget, state):
    if widget:
        widget.blockSignals(True)
        widget.setChecked(state in [1, '1', True, 'true'])
        widget.blockSignals(False)


def update_interface_with_communication_data(result, name):
    if result:
        (is_to_poll, description, description1, description2, description3,
         poll_until_found, no_transfer, befoerderung_ab, befoerderung_bis,
         poll_interval, escalation_timeout, pre_unzip, post_zip, rename_with_timestamp,
         gueltig_ab, gueltig_bis, find_pattern, quit_pattern, ack_pattern, zip_pattern,
         mov_pattern, put_pattern, rcv_pattern) = result

        name_input = next((widget for widget in QApplication.allWidgets() if
                           isinstance(widget, QLineEdit) and widget.objectName() == "name_input"), None)
        update_widget_text(name_input, name)

        polling_checkbox = next((widget for widget in QApplication.allWidgets() if
                                 isinstance(widget, QCheckBox) and widget.objectName() == "polling_activate_checkbox"), None)
        update_checkbox_state(polling_checkbox, is_to_poll)

        description_inputs = [description, description1, description2]
        for i, desc in enumerate(description_inputs, start=1):
            desc_input = next((widget for widget in QApplication.allWidgets() if
                               isinstance(widget, QLineEdit) and widget.objectName() == f"description_{i}_input"), None)
            update_widget_text(desc_input, desc)

        static_description_input = next((widget for widget in QApplication.allWidgets() if
                                          isinstance(widget, QLineEdit) and widget.objectName() == "description_input"), None)
        update_widget_text(static_description_input, description)

        poll_until_found_checkbox = next((widget for widget in QApplication.allWidgets() if
                                          isinstance(widget, QCheckBox) and widget.objectName() == "poll_until_found_checkbox"), None)
        update_checkbox_state(poll_until_found_checkbox, poll_until_found)

        no_transfer_checkbox = next((widget for widget in QApplication.allWidgets() if
                                     isinstance(widget, QCheckBox) and widget.objectName() == "no_transfer_checkbox"), None)
        update_checkbox_state(no_transfer_checkbox, no_transfer)

        fields = {
            "befoerderung_ab_input": befoerderung_ab,
            "befoerderung_bis_input": befoerderung_bis,
            "poll_interval_input": poll_interval,
            "escalation_timeout_input": escalation_timeout
        }

        for field_name, value in fields.items():
            field_widget = next((widget for widget in QApplication.allWidgets() if
                                 isinstance(widget, QLineEdit) and widget.objectName() == field_name), None)
            update_widget_text(field_widget, value)

        checkboxes = {
            "pre_unzip_checkbox": pre_unzip,
            "post_zip_checkbox": post_zip,
            "rename_with_timestamp_checkbox": rename_with_timestamp
        }

        for checkbox_name, state in checkboxes.items():
            checkbox_widget = next((widget for widget in QApplication.allWidgets() if
                                    isinstance(widget, QCheckBox) and widget.objectName() == checkbox_name), None)
            update_checkbox_state(checkbox_widget, state)

        valid_fields = {
            "gueltig_ab_input": gueltig_ab,
            "gueltig_bis_input": gueltig_bis
        }

        for field_name, value in valid_fields.items():
            field_widget = next((widget for widget in QApplication.allWidgets() if
                                 isinstance(widget, QLineEdit) and widget.objectName() == field_name), None)
            update_widget_text(field_widget, value)

        patterns = {
            "find_pattern_input": find_pattern,
            "quit_pattern_input": quit_pattern,
            "ack_pattern_input": ack_pattern,
            "zip_pattern_input": zip_pattern,
            "mov_pattern_input": mov_pattern,
            "put_pattern_input": put_pattern,
            "rcv_pattern_input": rcv_pattern
        }

        for pattern_name, pattern_value in patterns.items():
            pattern_widget = next((widget for widget in QApplication.allWidgets() if
                                   isinstance(widget, QLineEdit) and widget.objectName() == pattern_name), None)
            update_widget_text(pattern_widget, pattern_value)


def update_interface_with_source_data(source_result):
    source_input = next((widget for widget in QApplication.allWidgets() if
                         isinstance(widget, QLineEdit) and widget.objectName() == "source_input"), None)
    if source_input:
        update_widget_text(source_input, ", ".join(location[0] for location in source_result))


def update_interface_with_target_data(target_result):
    for i, (location, userid, password) in enumerate(target_result, start=1):
        target_location_input = next((widget for widget in QApplication.allWidgets() if
                                      isinstance(widget, QLineEdit) and widget.objectName() == f"target_{i}_input"),
                                     None)
        update_widget_text(target_location_input, location)

        user_id_input = next((widget for widget in QApplication.allWidgets() if
                              isinstance(widget, QLineEdit) and widget.objectName() == f"user_id_{i}_input"), None)
        update_widget_text(user_id_input, userid)

        password_input = next((widget for widget in QApplication.allWidgets() if
                               isinstance(widget, QLineEdit) and widget.objectName() == f"password_{i}_input"), None)
        update_widget_text(password_input, password)


def data_populating(name):
    conn = get_db_connection()
    cursor = conn.cursor()

    communication_result = fetch_communication_data(cursor, name)
    update_interface_with_communication_data(communication_result, name)

    source_result = fetch_source_locations(cursor, name)
    update_interface_with_source_data(source_result)

    target_result = fetch_target_locations(cursor, name)
    update_interface_with_target_data(target_result)

    fetch_alternate_name_list(cursor, name)

    conn.close()
