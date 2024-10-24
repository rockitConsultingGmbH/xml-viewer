from PyQt5.QtWidgets import QLineEdit
import logging

from common.connection_manager import ConnectionManager
from database.utils import insert_into_description, select_from_description, update_description

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class DescriptionTableData:
    def __init__(self, parent_widget=None):
        self.conn_manager = ConnectionManager().get_instance()
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

        # Find all QLineEdit fields
        all_line_edits = parent_widget.findChildren(QLineEdit)
        
        # Filter to get only those whose object name starts with 'description'
        description_fields = [field for field in all_line_edits if field.objectName().startswith('description')]
        
        return description_fields

    def save_description_data(self, communication_id, parent_widget=None):
        try:
            conn = self.conn_manager.get_db_connection()
            cursor = conn.cursor()

            # Get all fields that start with 'description'
            description_fields = self.get_all_description_fields(self.parent_widget)

            # Iterate through each found field and save data
            for field in description_fields:
                description_text = field.text()
                print(f"Found description field: {field.objectName()} with value: {description_text}")
                
                #if description_text:
                # Extract the ID from the field's object name (assuming it's in the format 'description_<id>_input')
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
