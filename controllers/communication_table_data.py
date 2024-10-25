import logging
from common.connection_manager import ConnectionManager
from common import config_manager
from database.utils import update_communication, select_from_communication
from controllers.utils.get_and_set_value import (get_text_value, set_checkbox_field, get_checkbox_value,
                                                convert_checkbox_to_string, set_text_field)

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class CommunicationTableData:
    def __init__(self, parent_widget=None):
        self.parent_widget = parent_widget
        self.conn_manager = ConnectionManager().get_instance()
        logging.debug("CommunicationTableData initialized with parent_widget: %s", parent_widget)

    def populate_communication_table_fields(self, communication_id, parent_widget=None):
        logging.debug("Populating communication table fields for communication_id: %s", communication_id)
        if parent_widget is None:
            parent_widget = self.parent_widget

        if parent_widget is None:
            logging.error("Parent widget must be provided either during initialization or as an argument.")
            raise ValueError("Parent widget must be provided either during initialization or as an argument.")

        conn = self.conn_manager.get_db_connection()
        cursor = conn.cursor()

        result = select_from_communication(cursor, communication_id, config_manager.config_id).fetchone()

        if result:
            logging.debug("Data fetched for communication_id: %s", communication_id)
            self.populate_fields(result)
        else:
            logging.warning("No data found for communication_id: %s", communication_id)
        conn.close()

    def populate_fields(self, result):
        logging.debug("Populating fields with data...")
        (name, is_to_poll, poll_until_found, no_transfer, befoerderung_ab, befoerderung_bis,
         poll_interval, escalation_timeout, pre_unzip, post_zip, rename_with_timestamp,
         gueltig_ab, gueltig_bis, find_pattern, quit_pattern, ack_pattern, zip_pattern,
         mov_pattern, put_pattern, rcv_pattern, tmp_pattern, alternate_name_list) = result

        set_text_field(self.parent_widget, "name_input", name)
        set_checkbox_field(self.parent_widget,"polling_activate_checkbox", is_to_poll)
        set_checkbox_field(self.parent_widget,"poll_until_found_checkbox", poll_until_found)
        set_checkbox_field(self.parent_widget,"no_transfer_checkbox", no_transfer)
        set_text_field(self.parent_widget, "befoerderung_ab_input", befoerderung_ab)
        set_text_field(self.parent_widget, "befoerderung_bis_input", befoerderung_bis)
        set_text_field(self.parent_widget, "poll_interval_input", poll_interval)
        set_text_field(self.parent_widget, "escalation_timeout_input", escalation_timeout)
        set_checkbox_field(self.parent_widget,"pre_unzip_checkbox", pre_unzip)
        set_checkbox_field(self.parent_widget,"post_zip_checkbox", post_zip)
        set_checkbox_field(self.parent_widget,"rename_with_timestamp_checkbox", rename_with_timestamp)
        set_text_field(self.parent_widget, "gueltig_ab_input", gueltig_ab)
        set_text_field(self.parent_widget, "gueltig_bis_input", gueltig_bis)
        set_text_field(self.parent_widget, "alt_name_input", alternate_name_list)

        self.populate_patterns(find_pattern, quit_pattern, ack_pattern, zip_pattern,
                               mov_pattern, put_pattern, rcv_pattern, tmp_pattern)

    def populate_patterns(self, *patterns, parent_widget=None):
        logging.debug("Populating patterns...")
        pattern_names = [
            "find_pattern_input", "quit_pattern_input", "ack_pattern_input",
            "zip_pattern_input", "mov_pattern_input", "put_pattern_input", "rcv_pattern_input",
            "tmp_pattern_input"
        ]

        for pattern_name, pattern_value in zip(pattern_names, patterns):
            set_text_field(self.parent_widget, pattern_name, pattern_value)

    def save_communication_data(self, communication_id):
        logging.debug("Saving communication data for communication_id: %s", communication_id)
        conn = self.conn_manager.get_db_connection()
        cursor = conn.cursor()

        communication_row = self.create_communication_row(communication_id)

        update_communication(cursor, communication_row)
        conn.commit()
        conn.close()
        logging.info("Communication data saved for communication_id: %s", communication_id)

    def create_communication_row(self, communication_id):
        logging.debug("Creating communication row for communication_id: %s", communication_id)
        return {
            'name': get_text_value(self.parent_widget,"name_input"),
            'alternateNameList': get_text_value(self.parent_widget,"alt_name_input"),
            'watcherEscalationTimeout': get_text_value(self.parent_widget,"escalation_timeout_input"),
            'isToPoll': convert_checkbox_to_string(get_checkbox_value(self.parent_widget,"polling_activate_checkbox")),
            'pollUntilFound': convert_checkbox_to_string(get_checkbox_value(self.parent_widget,"poll_until_found_checkbox")),
            'noTransfer': convert_checkbox_to_string(get_checkbox_value(self.parent_widget,"no_transfer_checkbox")),
            'targetMustBeArchived': '',
            'mustBeArchived': '',
            'historyDays': '',
            'targetHistoryDays': '',
            'findPattern': get_text_value(self.parent_widget,"find_pattern_input"),
            'movPattern': get_text_value(self.parent_widget,"mov_pattern_input"),
            'quitPattern': get_text_value(self.parent_widget,"quit_pattern_input"),
            'putPattern': get_text_value(self.parent_widget,"put_pattern_input"),
            'ackPattern': get_text_value(self.parent_widget,"ack_pattern_input"),
            'rcvPattern': get_text_value(self.parent_widget,"rcv_pattern_input"),
            'zipPattern': get_text_value(self.parent_widget,"zip_pattern_input"),
            'tmpPattern': get_text_value(self.parent_widget,"tmp_pattern_input"),
            'befoerderung': '',
            'pollInterval': get_text_value(self.parent_widget,"poll_interval_input"),
            'gueltigAb': get_text_value(self.parent_widget,"gueltig_ab_input"),
            'gueltigBis': get_text_value(self.parent_widget,"gueltig_bis_input"),
            'befoerderungAb': get_text_value(self.parent_widget,"befoerderung_ab_input"),
            'befoerderungBis': get_text_value(self.parent_widget,"befoerderung_bis_input"),
            'befoerderungCron': '',
            'preunzip': convert_checkbox_to_string(get_checkbox_value(self.parent_widget,"pre_unzip_checkbox")),
            'postzip': convert_checkbox_to_string(get_checkbox_value(self.parent_widget,"post_zip_checkbox")),
            'renameWithTimestamp': convert_checkbox_to_string(get_checkbox_value(self.parent_widget,"rename_with_timestamp_checkbox")),
            'communication_id': communication_id,
            'basicConfig_id': config_manager.config_id
        }
