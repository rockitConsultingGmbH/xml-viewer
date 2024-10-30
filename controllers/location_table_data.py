import logging
from common.connection_manager import ConnectionManager
from database.utils import delete_from_location, insert_into_location, update_location, select_from_location
from controllers.utils.get_and_set_value import (
                                                 get_checkbox_value,
                                                 convert_checkbox_to_string, get_text_value, set_checkbox_field, set_text_field)
from PyQt5.QtWidgets import QWidget

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LocationTableData:
    def __init__(self, parent_widget=None):
        self.parent_widget = parent_widget
        self.conn_manager = ConnectionManager().get_instance()
        logging.info("LocationTableData initialized with parent_widget: %s", parent_widget)

    def set_parent_widget(self, parent_widget):
        self.parent_widget = parent_widget
        logging.info("Parent widget set to: %s", parent_widget)

    # Source Location
    def populate_source_location_fields(self, communication_id, parent_widget=None, location_type='sourceLocation'):
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
        logging.info("Populating source fields with data....s")
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

    # Target Location
    def populate_target_location_fields(self, communication_id, parent_widget=None, location_type='targetLocation'):
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
                pass
                self.populate_target_fields(target_location)
        conn.close()
        logging.info("Target fields populated for communication_id: %s", communication_id)

    def populate_target_fields(self, target_location_row):
        logging.info("Populating target fields with data: %s", target_location_row)
        (id, communication_id, location, location_id, use_local_filename,
         use_path_from_config, target_must_be_archived, target_history_days,
         rename_existing_file, userid, password, description, location_type) = target_location_row
        
        self.parent_widget.setProperty("location_id", id)
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
        
        # Fetch existing locations from the database for the communication_id
        cursor = select_from_location(cursor, communication_id, location_type)
        existing_locations = {location['id']: location for location in cursor.fetchall()}
        logging.debug("Existing locations fetched: %s", existing_locations)

        # Get the list of locations from the GUI
        gui_locations = self.get_gui_target_locations() 
        logging.debug("GUI locations fetched: %s", gui_locations)

        #target_location_ids_to_delete =  get_target_location_ids_to_delete()
        #logging.debug("target_location_ids_to_delete", target_location_ids_to_delete)
        for location_data in gui_locations:
            location_id = location_data.get("id")

            # If location exists in the database, update it
            if location_id in existing_locations:
                location_row = self.create_target_location_row(location_data, communication_id, location_type)
                update_location(cursor, location_row)
                logging.info("Updated location with ID: %s", location_id)
            
            # If it's a new location, insert it
            else:
                new_location_row = self.create_target_location_row(location_data, communication_id, location_type, is_new=True)
                insert_into_location(cursor, new_location_row)
                logging.info("Inserted new location for communication_id: %s", communication_id)

        conn.commit()
        conn.close()
        logging.info("Target location data saved for communication_id: %s", communication_id)

    # Helper method to build a row dict for inserting or updating target locations
    def create_target_location_row(self, location_data, communication_id, location_type, is_new=False):
        logging.info("Creating target location row for communication_id: %s, location_type: %s", communication_id, location_type)
        row = {
            'location_id': location_data['location_id'],
            'location': location_data['location'],
            'userid': location_data['userid'],
            'password': location_data['password'],
            'useLocalFilename': convert_checkbox_to_string(location_data['useLocalFilename']),
            'usePathFromConfig': convert_checkbox_to_string(location_data['usePathFromConfig']),
            'targetMustBeArchived': convert_checkbox_to_string(location_data['targetMustBeArchived']),
            'targetHistoryDays': convert_checkbox_to_string(location_data['targetHistoryDays']),
            'renameExistingFile': convert_checkbox_to_string(location_data['renameExistingFile']),
            'description': location_data['description'],
            'locationType': location_type,
            'communication_id': communication_id,
        }

        if not is_new:  # If updating, include the primary key ID
            row['id'] = location_data['id']

        logging.debug("Created row: %s", row)
        return row

    def get_gui_target_locations(self):
        target_locations = []
        # Find all target box widgets that match "target_box_" in their object names
        target_boxes = [box for box in self.parent_widget.findChildren(QWidget) if box.objectName().startswith("target_box_")]
        
        for target_box in target_boxes:
            location_data = {}

            # Extract the target ID from the widget name
            target_id = target_box.property("target_id")
            location_data['id'] = target_id

            # Now retrieve the values within each target box widget
            location_data['location_id'] = get_text_value(target_box, f"location_id_target_{target_id}_input")
            location_data['location'] = get_text_value(target_box, f"target_{target_id}_input")
            location_data['userid'] = get_text_value(target_box, f"userid_target_{target_id}_input")
            location_data['password'] = get_text_value(target_box, f"password_target_{target_id}_input")
            
            # Retrieve checkbox values
            location_data['useLocalFilename'] = get_checkbox_value(target_box, f"use_local_filename_checkbox_target_{target_id}")
            location_data['usePathFromConfig'] = get_checkbox_value(target_box, f"use_path_from_config_checkbox_target_{target_id}")
            location_data['targetMustBeArchived'] = get_checkbox_value(target_box, f"target_must_be_archived_checkbox_{target_id}")
            location_data['targetHistoryDays'] = get_checkbox_value(target_box, f"target_history_days_checkbox_{target_id}")
            location_data['renameExistingFile'] = get_checkbox_value(target_box, f"rename_existing_file_checkbox_{target_id}")
            location_data['description'] = get_text_value(target_box, f"target_description_{target_id}_input")

            target_locations.append(location_data)

        return target_locations
    
    def delete_location_data(self, location_ids_to_delete):
        try:
            conn = self.conn_manager.get_db_connection()
            cursor = conn.cursor()

            for location_id in location_ids_to_delete:
                logging.debug(f"Deleting location with ID: {location_id}")
                delete_from_location(cursor, location_id)

            conn.commit()
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            conn.rollback()
        finally:
            conn.close()

