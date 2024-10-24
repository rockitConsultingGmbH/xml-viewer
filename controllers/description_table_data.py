from common.connection_manager import ConnectionManager
from database.utils import select_from_description, update_description
from controllers.utils.get_and_set_value import set_input_value, get_input_value
from PyQt5.QtWidgets import QLineEdit  # or from PySide2.QtWidgets import QLineEdit

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

    def save_description_data(self, parent_widget, communication_id):
        try:
            conn = self.conn_manager.get_db_connection()
            cursor = conn.cursor()
            rows = select_from_description(cursor, communication_id).fetchall()

            for row in rows():
                object_name = f"description_{row['id']}_input"
                input_field = parent_widget.findChild(QLineEdit, object_name)
                
                if input_field:
                    description_text = input_field.text()

                    if description_text:
                        description_id = row["id"]
                        description_row = {
                            'description_id': description_id,
                            'description': description_text,
                            'descriptionType': row['descriptionType']
                        }
                        update_description(cursor, description_row)

            conn.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            conn.rollback()
        finally:
            conn.close()
