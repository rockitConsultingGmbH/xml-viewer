from controllers.utils.get_db_connection import get_db_connection
from common import config_manager
from database.utils import update_communication, select_from_communication
from controllers.utils.get_and_set_value import (get_input_value, set_input_value, get_checkbox_value,
                                                 set_checkbox_value, convert_checkbox_to_string)


def populate_communication_table_fields(communication_id):
    conn, cursor = get_db_connection()

    result = select_from_communication(cursor, communication_id, config_manager.config_id)

    if result:
        populate_fields(result)

    conn.close()

def populate_fields(result):
    (name, is_to_poll, poll_until_found, no_transfer, befoerderung_ab, befoerderung_bis,
     poll_interval, escalation_timeout, pre_unzip, post_zip, rename_with_timestamp,
     gueltig_ab, gueltig_bis, find_pattern, quit_pattern, ack_pattern, zip_pattern,
     mov_pattern, put_pattern, rcv_pattern, alternate_name_list) = result

    set_input_value("name_input", name)
    set_checkbox_value("polling_activate_checkbox", is_to_poll)
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

    populate_patterns(find_pattern, quit_pattern, ack_pattern, zip_pattern, mov_pattern, put_pattern, rcv_pattern)
    set_input_value("alt_name_input", alternate_name_list)

def populate_patterns(*patterns):
    pattern_names = [
        "find_pattern_input", "quit_pattern_input", "ack_pattern_input",
        "zip_pattern_input", "mov_pattern_input", "put_pattern_input", "rcv_pattern_input"
    ]

    for pattern_name, pattern_value in zip(pattern_names, patterns):
        set_input_value(pattern_name, pattern_value)


def save_communication_data(communication_id):
    conn, cursor = get_db_connection()

    communication_row = create_communication_row(communication_id)

    update_communication(cursor, communication_row)
    conn.commit()
    conn.close()


def create_communication_row(communication_id):
    return {
        'name': get_input_value("name_input"),
        'alternateNameList': get_input_value("alt_name_input"),
        'watcherEscalationTimeout': get_input_value("escalation_timeout_input"),
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

