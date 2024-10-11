from PyQt5.QtWidgets import QApplication, QLineEdit, QCheckBox
from database.xml_to_db import get_db_connection


# Communication table
def fetch_record_data(cursor, record_id):
    cursor.execute(
        """SELECT name, isToPoll, pollUntilFound, noTransfer, befoerderungAb, befoerderungBis,
                  pollInterval, watcherEscalationTimeout, preunzip, postzip,
                  renameWithTimestamp, gueltigAb, gueltigBis, findPattern, quitPattern,
                  ackPattern, zipPattern, movPattern, putPattern, rcvPattern, alternateNameList
           FROM Communication WHERE id = ?""",
        (record_id,))
    return cursor.fetchone()


def set_input_value(widget_name, value):
    widget = next((widget for widget in QApplication.allWidgets() if
                   isinstance(widget, QLineEdit) and widget.objectName() == widget_name), None)
    if widget:
        widget.blockSignals(True)
        widget.setText(value or "")
        widget.blockSignals(False)


def set_checkbox_value(widget_name, value):
    checkbox = next((widget for widget in QApplication.allWidgets() if
                     isinstance(widget, QCheckBox) and widget.objectName() == widget_name), None)
    if checkbox:
        checkbox.blockSignals(True)
        checkbox.setChecked(value in [1, '1', True, 'true'])
        checkbox.blockSignals(False)


def data_populating(communication_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    result = fetch_record_data(cursor, communication_id)
    if result:
        (name, is_to_poll, poll_until_found, no_transfer, befoerderung_ab, befoerderung_bis,
         poll_interval, escalation_timeout, pre_unzip, post_zip, rename_with_timestamp,
         gueltig_ab, gueltig_bis, find_pattern, quit_pattern, ack_pattern, zip_pattern,
         mov_pattern, put_pattern, rcv_pattern, alternate_name_list) = result

        set_input_value("name_input", name)
        set_checkbox_value("polling_activate_checkbox", is_to_poll)

        # TODO: Implementation of filling description fields

        set_checkbox_value("poll_until_found_checkbox", poll_until_found)
        set_checkbox_value("no_transfer_checkbox", no_transfer)
        set_input_value("befoerderung_ab_input", befoerderung_ab)
        set_input_value("befoerderung_bis_input", befoerderung_bis)
        set_input_value("poll_interval_input", poll_interval)
        set_input_value("escalation_timeout_input", escalation_timeout)
        set_checkbox_value("pre_unzip_checkbox", pre_unzip)
        set_checkbox_value("post_zip_checkbox", post_zip)
        set_checkbox_value("rename_with_timestamp_checkbox", rename_with_timestamp)
        set_input_value("gueltig_ab_input", gueltig_ab)
        set_input_value("gueltig_bis_input", gueltig_bis)

        for pattern_name in ["find_pattern_input", "quit_pattern_input", "ack_pattern_input",
                             "zip_pattern_input", "mov_pattern_input", "put_pattern_input", "rcv_pattern_input"]:
            pattern_value = locals().get(pattern_name.replace("_input", ""))
            set_input_value(pattern_name, pattern_value)

        set_input_value("alt_name_input", alternate_name_list)

    conn.close()


def save_data(communication_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    name = get_input_value("name_input")
    is_to_poll = get_checkbox_value("polling_activate_checkbox")
    poll_until_found = get_checkbox_value("poll_until_found_checkbox")
    no_transfer = get_checkbox_value("no_transfer_checkbox")
    befoerderung_ab = get_input_value("befoerderung_ab_input")
    befoerderung_bis = get_input_value("befoerderung_bis_input")
    poll_interval = get_input_value("poll_interval_input")
    escalation_timeout = get_input_value("escalation_timeout_input")
    pre_unzip = get_checkbox_value("pre_unzip_checkbox")
    post_zip = get_checkbox_value("post_zip_checkbox")
    rename_with_timestamp = get_checkbox_value("rename_with_timestamp_checkbox")
    gueltig_ab = get_input_value("gueltig_ab_input")
    gueltig_bis = get_input_value("gueltig_bis_input")
    find_pattern = get_input_value("find_pattern_input")
    quit_pattern = get_input_value("quit_pattern_input")
    ack_pattern = get_input_value("ack_pattern_input")
    zip_pattern = get_input_value("zip_pattern_input")
    mov_pattern = get_input_value("mov_pattern_input")
    put_pattern = get_input_value("put_pattern_input")
    rcv_pattern = get_input_value("rcv_pattern_input")
    alternate_name_list = get_input_value("alt_name_input")

    if name is None or name.strip() == "":
        conn.close()
        return

    try:
        cursor.execute(
            """UPDATE Communication
               SET name = ?, isToPoll = ?, pollUntilFound = ?, noTransfer = ?, befoerderungAb = ?, befoerderungBis = ?,
                   pollInterval = ?, watcherEscalationTimeout = ?, preunzip = ?, postzip = ?,
                   renameWithTimestamp = ?, gueltigAb = ?, gueltigBis = ?, findPattern = ?, quitPattern = ?,
                   ackPattern = ?, zipPattern = ?, movPattern = ?, putPattern = ?, rcvPattern = ?, alternateNameList = ?
               WHERE id = ?""",
            (name, is_to_poll, poll_until_found, no_transfer, befoerderung_ab,
             befoerderung_bis, poll_interval, escalation_timeout, pre_unzip, post_zip,
             rename_with_timestamp, gueltig_ab, gueltig_bis, find_pattern,
             quit_pattern, ack_pattern, zip_pattern, mov_pattern, put_pattern,
             rcv_pattern, alternate_name_list, communication_id)
        )

        conn.commit()
    except Exception as e:
        print(f"Error while saving data: {e}")
    finally:
        conn.close()


def get_input_value(widget_name):
    widget = next((widget for widget in QApplication.allWidgets() if
                   isinstance(widget, QLineEdit) and widget.objectName() == widget_name), None)
    return widget.text() if widget else ""


def get_checkbox_value(widget_name):
    checkbox = next((widget for widget in QApplication.allWidgets() if
                     isinstance(widget, QCheckBox) and widget.objectName() == widget_name), None)
    return checkbox.isChecked() if checkbox else False
