from PyQt5.QtWidgets import QLineEdit

from common.connection_manager import ConnectionManager
from database.utils import insert_into_description, select_from_description, update_description

class DescriptionTableData:
    def __init__(self):
        self.conn_manager = ConnectionManager().get_instance()

    def populate_description_fields(self, parent_widget, communication_id):
        conn = self.conn_manager.get_db_connection()
        cursor = conn.cursor()
        rows = select_from_description(cursor, communication_id).fetchall()

        for row in rows:
            object_name = f"description_{row['id']}_input"
            input_field = parent_widget.findChild(QLineEdit, object_name)
            
            if input_field:
                input_field.setText(row["description"])
            else:
                print(f"Input field {object_name} not found")

        conn.close()


    def get_all_description_fields(self, parent_widget):
        # Find all QLineEdit fields
        all_line_edits = parent_widget.findChildren(QLineEdit)
        
        # Filter to get only those whose object name starts with 'description'
        description_fields = [field for field in all_line_edits if field.objectName().startswith('description')]
        
        return description_fields


    def save_description_data(self, parent_widget, communication_id):
        try:
            conn = self.conn_manager.get_db_connection()
            cursor = conn.cursor()

            # Get all fields that start with 'description'
            description_fields = self.get_all_description_fields(parent_widget)

            # Iterate through each found field and save data
            for field in description_fields:
                description_text = field.text()
                print(f"Found description field: {field.objectName()} with value: {description_text}")
                
                if description_text:
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
                    else:
                        insert_into_description(cursor, {'communication_id': communication_id, 'description': description_text, 'descriptionType': 'description'} )

            conn.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            conn.rollback()
        finally:
            conn.close()
