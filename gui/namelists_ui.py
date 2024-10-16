from PyQt5.QtWidgets import (QVBoxLayout, QFormLayout,
                             QLineEdit, QWidget, QScrollArea, QLabel, QFrame)
from PyQt5.QtCore import Qt
from common.connection_manager import ConnectionManager
from database.utils import select_from_alternatename, select_from_namelist
from gui.popup_message_ui import PopupMessage
from gui.buttons import ButtonFactory

class NameListsWidget(QWidget):
    def __init__(self, nameList_id=None, parent=None):
        super().__init__(parent)
        self.nameList_id = str(nameList_id) if nameList_id is not None else ""
        self.conn_manager = ConnectionManager().get_instance()
        self.popup_message = PopupMessage(self)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Add button layout (assumed you have this function)
        button_layout = ButtonFactory().create_button_layout(self)
        layout.addLayout(button_layout)

        # Create a NameList section
        self.create_namelist_layout(layout)

        # Add a divider
        self.add_divider(layout, "Alternate Names")

        # Create the AlternateName entries section
        self.create_name_entries_layout(layout)

        # Set the main layout
        self.setLayout(layout)

    def create_namelist_layout(self, parent_layout):
        namelist_layout = QFormLayout()
        self.init_namelist_input_fields()
        self.add_namelist_fields_to_form_layout(namelist_layout)
        self.populate_namelist_fields_from_db()
        parent_layout.addLayout(namelist_layout)

    def add_divider(self, layout, text):
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        layout.addWidget(divider)

    def create_name_entries_layout(self, parent_layout):
        # Create a widget to hold the layout
        entries_widget = QWidget()
        name_entries_layout = QVBoxLayout(entries_widget)

        # Set consistent spacing and margins
        name_entries_layout.setSpacing(10)  # Set spacing between entries
        name_entries_layout.setContentsMargins(10, 10, 10, 10)  # Set layout margins

        # Fetch name entries data
        name_entries = self.get_name_entries_data()

        # Loop through each entry and create a form layout for it
        for entry in name_entries:
            entry_layout = QFormLayout()
            entry_layout.setSpacing(5)  # Consistent spacing for entry layouts
            self.add_name_entries_fields_to_form_layout(entry_layout, entry)
            name_entries_layout.addLayout(entry_layout)

        # Wrap the entries layout in a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(entries_widget)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # Only show scroll bar if needed

        # Add the scroll area to the parent layout
        parent_layout.addWidget(scroll_area)

    def add_name_entries_fields_to_form_layout(self, form_layout, entry):
        entry_input = QLineEdit(entry["entry"])
        entry_input.setFixedWidth(300)  # Set a fixed width for consistent field alignment
        form_layout.addRow("Entry:", entry_input)

    def set_fields_from_db(self):
        try:
            self.populate_name_entries_fields_from_db()
        except Exception as e:
            print(f"Error populating fields from database: {e}")
            self.popup_message.show_message("Error populating fields from database.")
         
    def save_fields_to_db(self):
        try:
            conn = self.conn_manager.get_db_connection()
            cursor = conn.cursor()
            # Placeholder for future save functionality
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

    def init_namelist_input_fields(self):
        # Initialize input fields for the NameList table (e.g., listName)
        self.list_name_input = QLineEdit()
        self.list_name_input.setFixedWidth(300)  # Set a fixed width for consistent field alignment
        
    def add_namelist_fields_to_form_layout(self, form_layout):
        form_layout.addRow("Name:", self.list_name_input)

    def populate_namelist_fields_from_db(self):
        conn = self.conn_manager.get_db_connection()
        cursor = conn.cursor()
        cursor = select_from_namelist(cursor, self.nameList_id)  #execute("SELECT listName FROM NameList WHERE id = ?", (self.nameList_id,))
        result = cursor.fetchone()
        if result:
            print(result["listName"])
            self.list_name_input.setText(result["listName"])
        conn.close()
