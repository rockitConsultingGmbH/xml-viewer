from PyQt5.QtWidgets import (QVBoxLayout, QFormLayout,
                             QLineEdit, QWidget, QScrollArea)
from common.connection_manager import ConnectionManager
from database.utils import select_from_alternatename
from gui.popup_message_ui import PopupMessage
from gui.buttons import create_button_layout

class NameListsWidget(QWidget):
    def __init__(self, nameList_id=None, parent=None):
        super().__init__(parent)
        self.nameList_id = str(nameList_id) if nameList_id is not None else ""
        self.conn_manager = ConnectionManager().get_instance()
        self.popup_message = PopupMessage(self)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        button_layout = create_button_layout(self)
        layout.addLayout(button_layout)

        #self.create_namelist_layout(layout)
        self.create_name_entries_layout(layout) 
        #self.set_input_field_sizes()

        self.setLayout(layout)

    def create_namelist_layout(self, parent_layout):
        namelist_layout = QFormLayout()
        self.init_namelist_input_fields()
        self.add_namelist_fields_to_form_layout(namelist_layout)
        self.populate_namelist_fields_from_db()
        parent_layout.addLayout(namelist_layout)
        
    def create_name_entries_layout(self, parent_layout):
        name_entries_layout = QVBoxLayout()
        name_entries = self.get_name_entries_data()

        # Loop through each entry and create a form layout for it
        for entry in name_entries:
            entry_layout = QFormLayout()
            self.add_name_entries_fields_to_form_layout(entry_layout, entry)
            name_entries_layout.addLayout(entry_layout)

        # Wrap the layout in a scroll area if needed
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(QWidget())
        scroll_area.widget().setLayout(name_entries_layout)
        parent_layout.addWidget(scroll_area)
  
    def add_name_entries_fields_to_form_layout(self, form_layout, entry):
        # Add input fields for a single IPQueue entry
        entry_input = QLineEdit(entry["entry"])

        form_layout.addRow("Entry:", entry_input)

    def populate_fields_from_db(self):
        try:
            self.populate_name_entries_fields_from_db()
        except Exception as e:
            print(f"Error populating fields from database: {e}")
            self.popup_message.show_message("Error populating fields from database.")
         
    def save_fields_to_db(self):
        try:
            conn = self.conn_manager.get_db_connection()
            cursor = conn.cursor()
            pass #TODO: Implement saving fields to database
            conn.commit()
            self.popup_message.show_message("Changes in MQ Configuration have been successfully saved.")
        except Exception as e:
            print(f"Error while saving data: {e}")
            conn.rollback()
            self.popup_message.show_error_message(f"Error while saving data: {e}")
        finally:
            conn.close()

    def populate_name_entries_fields_from_db(self):
        data = self.get_name_entries_data()
        if data:
            self.entry_input.setText(data["entry"])
            
    def get_name_entries_data(self):
        conn = self.conn_manager.get_db_connection()
        cursor = conn.cursor()
        cursor = select_from_alternatename(cursor, self.nameList_id) 
        rows = cursor.fetchall()
        conn.close()
        return rows
