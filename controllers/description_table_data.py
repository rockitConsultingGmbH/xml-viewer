from PyQt5.QtWidgets import QLineEdit
import logging

from common.connection_manager import ConnectionManager
from database.utils import delete_from_description, insert_into_description, select_from_description, update_description

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class DescriptionTableData:
    def __init__(self, parent_widget=None):
        self.conn_manager = ConnectionManager()
        self.parent_widget = parent_widget

    def set_parent_widget(self, parent_widget):
        self.parent_widget = parent_widget

    def populate_description_fields(self, communication_id, parent_widget=None):
        if parent_widget is None:
            parent_widget = self.parent_widget

        if parent_widget is None:
            raise ValueError("Parent widget must be provided either during initialization or as an argument.")

        try:
            conn = self.conn_manager.get_db_connection()
            cursor = conn.cursor()
            rows = select_from_description(cursor, communication_id).fetchall()
        except Exception as e:
            logging.error(f"An error occurred while fetching descriptions: {e}")
            return

        for row in rows:
            object_name = f"description_{row['id']}_input"
            input_field = parent_widget.findChild(QLineEdit, object_name)
            
            if input_field:
                input_field.setText(row["description"])
            else:
                logging.warning(f"Input field {object_name} not found")

        conn.close()

    def get_all_description_fields(self, parent_widget=None):
        if parent_widget is None:
            parent_widget = self.parent_widget

        if parent_widget is None:
            raise ValueError("Parent widget must be provided either during initialization or as an argument.")

        all_line_edits = parent_widget.findChildren(QLineEdit)
        
        description_fields = [field for field in all_line_edits if field.objectName().startswith('description')]
        
        return description_fields

    def save_description_data(self, communication_id, parent_widget=None):
        try:
            conn = self.conn_manager.get_db_connection()
            cursor = conn.cursor()

            description_fields = self.get_all_description_fields(self.parent_widget)

            for field in description_fields:
                description_text = field.text()
                logging.debug(f"Found description field: {field.objectName()} with value: {description_text}")
                
                description_id = field.objectName().split('_')[1]
                existing_result = select_from_description(cursor, communication_id, description_id).fetchone()

                if existing_result:
                    description_row = {
                        'description_id': description_id,
                        'description': description_text,
                        'descriptionType': existing_result['descriptionType']
                    }
                    update_description(cursor, description_row)
                elif description_text:
                    insert_into_description(cursor, {'communication_id': communication_id, 'description': description_text, 'descriptionType': 'description'})

            conn.commit()
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            conn.rollback()
        finally:
            conn.close()

    def delete_description_data(self, description_ids_to_delete):
        try:
            conn = self.conn_manager.get_db_connection()
            cursor = conn.cursor()

            for description_id in description_ids_to_delete:
                logging.debug(f"Deleting description with ID: {description_id}")
                delete_from_description(cursor, description_id)

            conn.commit()
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            conn.rollback()
        finally:
            conn.close()
