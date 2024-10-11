from PyQt5.QtWidgets import QApplication, QLineEdit, QCheckBox
from common import config_manager
from controllers.connection_manager import ConnectionManager
from database.utils import update_communication

# Communication table
def fetch_record_data(cursor, record_id):
    cursor.execute(
        """SELECT name, isToPoll, pollUntilFound, noTransfer, befoerderungAb, befoerderungBis,
                  pollInterval, watcherEscalationTimeout, preunzip, postzip,
                  renameWithTimestamp, gueltigAb, gueltigBis, findPattern, quitPattern,
                  ackPattern, zipPattern, movPattern, putPattern, rcvPattern, alternateNameList
           FROM Communication WHERE id = ? AND basicConfig_id = ?""",
        (record_id, config_manager.config_id))
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
    conn_manager = ConnectionManager().get_instance()
    conn = conn_manager.get_db_connection()
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
    conn_manager = ConnectionManager().get_instance()
    conn = conn_manager.get_db_connection()
    cursor = conn.cursor()
    name = get_input_value("name_input"),

    print(f"Saving data for communication_id: {communication_id}")
    print(f"Saving data for config_id: {config_manager.config_id}")
    communication_row = {
        'name': get_input_value("name_input"),
        'alternateNameList': get_input_value("alt_name_input"),
        'watcherEscalationTimeout':  get_input_value("escalation_timeout_input"),
        'isToPoll': convert_checkbox_to_string(get_checkbox_value("polling_activate_checkbox")),
        'pollUntilFound': convert_checkbox_to_string(get_checkbox_value("poll_until_found_checkbox")),
        'noTransfer': convert_checkbox_to_string(get_checkbox_value("no_transfer_checkbox")),
        'targetMustBeArchived': '',
        'mustBeArchived': '',
        'historyDays': '',
        'targetHistoryDays': '',
        'findPattern': get_input_value("find_pattern_input"),
        'movPattern': get_input_value("mov_pattern_input"),
        'tmpPattern': '',
        'quitPattern': get_input_value("quit_pattern_input"),
        'putPattern': get_input_value("put_pattern_input"),
        'ackPattern': get_input_value("ack_pattern_input"),
        'rcvPattern': get_input_value("rcv_pattern_input"),
        'zipPattern': get_input_value("zip_pattern_input"),
        'befoerderung': '',
        'pollInterval': get_input_value("poll_interval_input"),
        'gueltigAb': get_input_value("gueltig_ab_input"),
        'gueltigBis': get_input_value("gueltig_bis_input"),
        'befoerderungAb': get_input_value("befoerderung_ab_input"),
        'befoerderungBis': get_input_value("befoerderung_bis_input"),
        'befoerderungCron': '',
        'preunzip': convert_checkbox_to_string(get_checkbox_value("pre_unzip_checkbox")),
        'postzip': convert_checkbox_to_string(get_checkbox_value("post_zip_checkbox")),
        'renameWithTimestamp': convert_checkbox_to_string(get_checkbox_value("rename_with_timestamp_checkbox")),
        'communication_id': communication_id,
        'basicConfig_id': config_manager.config_id
    }	

    #if name is None or name.strip() == "":
    #    conn.close()
    #    return

    try:
        update_communication(cursor, communication_row)
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

def convert_checkbox_to_string(checkbox_value):    return "true" if checkbox_value else "false"