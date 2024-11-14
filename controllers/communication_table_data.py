import logging
from common.connection_manager import ConnectionManager
from common.config_manager import ConfigManager
from database.utils import update_communication, select_from_communication, \
    get_communication_names
from controllers.utils.get_and_set_value import (get_text_value, set_checkbox_field, get_checkbox_value,
                                                convert_checkbox_to_string, set_text_field, set_label)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class CommunicationTableData:
    def __init__(self, parent_widget=None):
        self.parent_widget = parent_widget
        self.conn_manager = ConnectionManager()
        self.config_manager = ConfigManager()
        logging.debug("CommunicationTableData initialized with parent_widget: %s", parent_widget)

    def get_communication_name(self, communication_id):
        try:
            conn = self.conn_manager.get_db_connection()
            cursor = conn.cursor()

            cursor = get_communication_names(cursor, communication_id, self.config_manager.config_id)
            result = cursor.fetchone()

            if result:
                return result['name']
            return None

        except Exception as e:
            print(f"Error while getting communication name: {e}")
            return None
        finally:
            conn.close()

    def populate_communication_table_fields(self, communication_id, parent_widget=None):
        logging.debug("Populating communication table fields for communication_id: %s", communication_id)
        if parent_widget is None:
            parent_widget = self.parent_widget

        if parent_widget is None:
            logging.error("Parent widget must be provided either during initialization or as an argument.")
            raise ValueError("Parent widget must be provided either during initialization or as an argument.")

        conn = self.conn_manager.get_db_connection()
        cursor = conn.cursor()

        row = select_from_communication(cursor, communication_id, self.config_manager.config_id).fetchone()

        if row:
            logging.debug("Data fetched for communication_id: %s", communication_id)
            self.populate_fields(row)
        else:
            logging.warning("No data found for communication_id: %s", communication_id)
        conn.close()

    def populate_fields(self, row):
        logging.debug("Populating fields with data...")

        set_text_field(self.parent_widget, "name_input", row['name'])
        set_checkbox_field(self.parent_widget,"polling_activated_checkbox", row['isToPoll'])
        set_label(self.parent_widget, "polling_status", f"Polling aktiviert: {row['isToPoll']}")
        set_checkbox_field(self.parent_widget,"poll_until_found_checkbox", row['pollUntilFound'])
        set_checkbox_field(self.parent_widget,"no_transfer_checkbox", row['noTransfer'])
        set_text_field(self.parent_widget, "befoerderung_ab_input", row['befoerderungAb'])
        set_text_field(self.parent_widget, "befoerderung_bis_input", row['befoerderungBis'])
        set_text_field(self.parent_widget, "befoerderung_cron_input", row['befoerderungCron'])
        set_text_field(self.parent_widget, "poll_interval_input", row['pollInterval'])
        set_text_field(self.parent_widget, "escalation_timeout_input", row['watcherEscalationTimeout'])
        set_checkbox_field(self.parent_widget,"pre_unzip_checkbox", row['preunzip'])
        set_checkbox_field(self.parent_widget,"post_zip_checkbox", row['postzip'])
        set_checkbox_field(self.parent_widget,"target_must_be_archived_checkbox", row['targetMustBeArchived'])
        set_checkbox_field(self.parent_widget,"must_be_archived_checkbox", row['mustBeArchived'])
        set_text_field(self.parent_widget,"target_history_days_input", row['targetHistoryDays'])
        set_text_field(self.parent_widget,"history_days_input", row['historyDays'])
        set_checkbox_field(self.parent_widget,"rename_with_timestamp_checkbox", row['renameWithTimestamp'])
        set_text_field(self.parent_widget, "gueltig_ab_input", row['gueltigAb'])
        set_text_field(self.parent_widget, "gueltig_bis_input", row['gueltigBis'])
        set_text_field(self.parent_widget, "alt_name_input", row['alternateNameList'])

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
            'isToPoll': convert_checkbox_to_string(get_checkbox_value(self.parent_widget,"polling_activated_checkbox")),
            'pollUntilFound': convert_checkbox_to_string(get_checkbox_value(self.parent_widget,"poll_until_found_checkbox")),
            'noTransfer': convert_checkbox_to_string(get_checkbox_value(self.parent_widget,"no_transfer_checkbox")),
            'targetMustBeArchived': convert_checkbox_to_string(get_checkbox_value(self.parent_widget,"target_must_be_archived_checkbox")),
            'targetHistoryDays': get_text_value(self.parent_widget,"target_history_days_input"),
            'mustBeArchived': convert_checkbox_to_string(get_checkbox_value(self.parent_widget,"must_be_archived_checkbox")),
            'historyDays':  get_text_value(self.parent_widget,"history_days_input"),
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
            'befoerderungCron': get_text_value(self.parent_widget,"befoerderung_cron_input"),
            'preunzip': convert_checkbox_to_string(get_checkbox_value(self.parent_widget,"pre_unzip_checkbox")),
            'postzip': convert_checkbox_to_string(get_checkbox_value(self.parent_widget,"post_zip_checkbox")),
            'renameWithTimestamp': convert_checkbox_to_string(get_checkbox_value(self.parent_widget,"rename_with_timestamp_checkbox")),
            'communication_id': communication_id,
            'basicConfig_id': self.config_manager.config_id
        }


