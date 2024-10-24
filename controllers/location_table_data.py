import logging
from common.connection_manager import ConnectionManager
from database.utils import update_location, select_from_location
from controllers.utils.get_and_set_value import (get_input_value,
                                                 get_checkbox_value,
                                                 convert_checkbox_to_string, get_text_value, set_checkbox_field, set_text_field)
from PyQt5.QtWidgets import QLineEdit, QCheckBox

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LocationTableData:
    def __init__(self, parent_widget=None):
        self.conn_manager = ConnectionManager().get_instance()
        self.parent_widget = parent_widget
        logging.info("LocationTableData initialized with parent_widget: %s", parent_widget)

    def set_parent_widget(self, parent_widget):
        self.parent_widget = parent_widget
        logging.info("Parent widget set to: %s", parent_widget)

    def populate_location_source_fields(self, communication_id, parent_widget=None, location_type='sourceLocation'):
        if parent_widget is None:
            parent_widget = self.parent_widget

        if parent_widget is None:
            raise ValueError("Parent widget must be provided either during initialization or as an argument.")

        logging.info("Populating source fields for communication_id: %s, location_type: %s", communication_id, location_type)
        conn = self.conn_manager.get_db_connection()
        cursor = conn.cursor()
        source_location_row = select_from_location(cursor, communication_id, location_type).fetchone()
        if source_location_row:
            self.populate_source_fields(source_location_row)
        conn.close()
        logging.info("Source fields populated for communication_id: %s", communication_id)

    def populate_source_fields(self, source_location_row):
        logging.info("Populating source fields with data: %s", source_location_row)
        (id, communication_id, location, location_id, use_local_filename,
         use_path_from_config, target_must_be_archived, target_history_days,
         rename_existing_file, userid, password, description, location_type) = source_location_row

        set_text_field(self.parent_widget, "source_input", location)
        set_text_field(self.parent_widget, "userid_source_input", userid)
        set_text_field(self.parent_widget, "password_source_input", password)
        set_text_field(self.parent_widget, "source_description_input", description)
        set_text_field(self.parent_widget, "location_id_input", location_id)
        set_checkbox_field(self.parent_widget, "use_local_filename_checkbox", use_local_filename)
        set_checkbox_field(self.parent_widget, "use_path_from_config_checkbox", use_path_from_config)
        set_checkbox_field(self.parent_widget, "target_history_days_checkbox", target_history_days)
        set_checkbox_field(self.parent_widget, "rename_existing_file_checkbox", rename_existing_file)
        set_checkbox_field(self.parent_widget, "target_must_be_archived_checkbox", target_must_be_archived)

    def save_source_location_data(self, communication_id, location_type='sourceLocation'):
        logging.info("Saving source location data for communication_id: %s, location_type: %s", communication_id, location_type)
        conn = self.conn_manager.get_db_connection()
        cursor = conn.cursor()
        source_location = select_from_location(cursor, communication_id, location_type).fetchone()
        if source_location:
            location_row = self.create_source_location_row(source_location, communication_id, location_type)
            logging.info("Location row created: %s", location_row)
            try:
                update_location(cursor, location_row)
                conn.commit()
            except Exception as e:
                logging.error(f"An error occurred while updating source location: {e}")
                conn.rollback()
        conn.close()
        logging.info("Source location data saved for communication_id: %s", communication_id)

    def create_source_location_row(self, source_location, communication_id, location_type):
        logging.info("Creating source location row for communication_id: %s, location_type: %s", communication_id, location_type)
        return {
            'id': source_location[0],
            'location_id': get_text_value(self.parent_widget, "location_id_input"),
            'location': get_text_value(self.parent_widget, "source_input"),
            'userid': get_text_value(self.parent_widget,"userid_source_input"),
            'password': get_text_value(self.parent_widget, "password_source_input"),
            'useLocalFilename': convert_checkbox_to_string(get_checkbox_value(self.parent_widget,"use_local_filename_checkbox")),
            'usePathFromConfig': convert_checkbox_to_string(get_checkbox_value(self.parent_widget,"use_path_from_config_checkbox")),
            'targetMustBeArchived': convert_checkbox_to_string(get_checkbox_value(self.parent_widget,"target_must_be_archived_checkbox")),
            'targetHistoryDays': convert_checkbox_to_string(get_checkbox_value(self.parent_widget,"target_history_days_checkbox")),
            'renameExistingFile': convert_checkbox_to_string(get_checkbox_value(self.parent_widget,"rename_existing_file_checkbox")),
            'description': get_text_value(self.parent_widget,"source_description_input"),
            'locationType': location_type,
            'communication_id': communication_id,
        }

    def populate_location_target_fields(self, communication_id, parent_widget=None, location_type='targetLocation'):
        if parent_widget is None:
            parent_widget = self.parent_widget

        if parent_widget is None:
            raise ValueError("Parent widget must be provided either during initialization or as an argument.")

        logging.info("Populating target fields for communication_id: %s, location_type: %s", communication_id, location_type)
        conn = self.conn_manager.get_db_connection()
        cursor = conn.cursor()
        target_locations = select_from_location(cursor, communication_id, location_type).fetchall()
        for target_location in target_locations:
            if target_location:
                self.populate_target_fields(target_location)
        conn.close()
        logging.info("Target fields populated for communication_id: %s", communication_id)

    def populate_target_fields(self, target_location_row):
        logging.info("Populating target fields with data: %s", target_location_row)
        (id, communication_id, location, location_id, use_local_filename,
         use_path_from_config, target_must_be_archived, target_history_days,
         rename_existing_file, userid, password, description, location_type) = target_location_row

        set_text_field(self.parent_widget, f"target_{id}_input", location)
        set_text_field(self.parent_widget, f"userid_target_{id}_input", userid)
        set_text_field(self.parent_widget, f"password_target_{id}_input", password)
        set_text_field(self.parent_widget, f"target_description_{id}_input", description)
        set_text_field(self.parent_widget, f"location_id_target_{id}_input", location_id)
        set_checkbox_field(self.parent_widget, f"use_local_filename_checkbox_target_{id}", use_local_filename)
        set_checkbox_field(self.parent_widget, f"use_path_from_config_checkbox_target_{id}", use_path_from_config)
        set_checkbox_field(self.parent_widget, f"target_history_days_checkbox_{id}", target_history_days)
        set_checkbox_field(self.parent_widget, f"rename_existing_file_checkbox_{id}", rename_existing_file)
        set_checkbox_field(self.parent_widget, f"target_must_be_archived_checkbox_{id}", target_must_be_archived)

    def save_target_location_data(self, communication_id, location_type='targetLocation'):
        logging.info("Saving target location data for communication_id: %s, location_type: %s", communication_id, location_type)
        conn = self.conn_manager.get_db_connection()
        cursor = conn.cursor()
        cursor = select_from_location(cursor, communication_id, location_type)
        target_locations = cursor.fetchall()
        if target_locations:
            for target_location in target_locations:
                location_row = self.create_target_location_row(target_location, communication_id, location_type)
                update_location(cursor, location_row)
            conn.commit()
        conn.close()
        logging.info("Target location data saved for communication_id: %s", communication_id)

    def create_target_location_row(self, target_location, communication_id, location_type):
        logging.info("Creating target location row for communication_id: %s, location_type: %s", communication_id, location_type)
        return {
            'id': target_location[0],
            'location_id': get_input_value(self.parent_widget, f"location_id_target_{target_location[0]}_input"),
            'location': get_input_value(self.parent_widget, f"target_{target_location[0]}_input"),
            'userid': get_input_value(self.parent_widget, f"userid_target_{target_location[0]}_input"),
            'password': get_input_value(self.parent_widget, f"password_target_{target_location[0]}_input"),
            'useLocalFilename': convert_checkbox_to_string(
                get_checkbox_value(self.parent_widget, f"use_local_filename_checkbox_target_{target_location[0]}")),
            'usePathFromConfig': convert_checkbox_to_string(
                get_checkbox_value(self.parent_widget, f"use_path_from_config_checkbox_target_{target_location[0]}")),
            'targetMustBeArchived': convert_checkbox_to_string(
                get_checkbox_value(self.parent_widget, f"target_must_be_archived_checkbox_{target_location[0]}")),
            'targetHistoryDays': convert_checkbox_to_string(
                get_checkbox_value(self.parent_widget, f"target_history_days_checkbox_{target_location[0]}")),
            'renameExistingFile': convert_checkbox_to_string(
                get_checkbox_value(self.parent_widget, f"rename_existing_file_checkbox_{target_location[0]}")),
            'description': get_input_value(self.parent_widget, f"target_description_{target_location[0]}_input"),
            'locationType': location_type,
            'communication_id': communication_id,
        }
