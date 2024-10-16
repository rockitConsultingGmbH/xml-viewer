from PyQt5.QtWidgets import (QVBoxLayout, QFormLayout, QLineEdit, QWidget, QScrollArea, QLabel, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal
from common.connection_manager import ConnectionManager
from database.utils import select_from_alternatename, select_from_namelist
from gui.popup_message_ui import PopupMessage
from gui.components.buttons import ButtonFactory

class NameListsWidget(QWidget):
    name_updated = pyqtSignal(int, str)  # Signal to notify when the name is updated

    def __init__(self, nameList_id=None, parent=None):
        super().__init__(parent)
        self.nameList_id = str(nameList_id) if nameList_id is not None else ""
        self.conn_manager = ConnectionManager().get_instance()
        self.popup_message = PopupMessage(self)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.addLayout(ButtonFactory().create_button_layout(self))
        self.create_namelist_layout(layout)
        self.add_divider(layout, "Alternate Names")
        self.create_name_entries_layout(layout)
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
        entries_widget = QWidget()
        self.name_entries_layout = QVBoxLayout(entries_widget)
        self.name_entries_layout.setSpacing(10)
        self.name_entries_layout.setContentsMargins(10, 10, 10, 10)

        name_entries = self.get_name_entries_data()
        for entry in name_entries:
            entry_layout = QFormLayout()
            entry_layout.setSpacing(5)
            self.add_name_entries_fields_to_form_layout(entry_layout, entry)
            self.name_entries_layout.addLayout(entry_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidget(entries_widget)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        parent_layout.addWidget(scroll_area)

    def add_name_entries_fields_to_form_layout(self, form_layout, entry):
        entry_label = QLabel("Entry:")
        entry_input = QLineEdit(entry["entry"])
        entry_input.setFixedWidth(300)

        entry_input.setProperty("entry_id", entry["id"])
        form_layout.addRow(entry_label, entry_input)

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

            # Save or update the NameList table
            list_name = self.list_name_input.text()

            if self.nameList_id:
                # Update existing NameList if nameList_id is present
                cursor.execute("""
                    UPDATE NameList 
                    SET listName = ? 
                    WHERE id = ?
                """, (list_name, self.nameList_id))
            else:
                # Insert new entry into NameList if no nameList_id is provided
                cursor.execute("""
                    INSERT INTO NameList (listName) 
                    VALUES (?)
                """, (list_name,))
                self.nameList_id = cursor.lastrowid

            # Save or update the AlternateName table for each entry
            for layout in self.name_entries_layout.children():
                if isinstance(layout, QFormLayout):
                    entry_field = layout.itemAt(1).widget()  # Get the QLineEdit
                    entry_value = entry_field.text()

                    # Retrieve the entry ID from the field's property
                    entry_id = entry_field.property("entry_id")

                    if entry_value:  # Only save non-empty entries
                        if entry_id:  # If entry ID exists, update the existing entry
                            cursor.execute("""
                                UPDATE AlternateName 
                                SET entry = ? 
                                WHERE id = ?
                            """, (entry_value, entry_id))
                        else:
                            # Entry doesn't exist, insert new
                            cursor.execute("""
                                INSERT INTO AlternateName (nameList_id, entry) 
                                VALUES (?, ?)
                            """, (self.nameList_id, entry_value))

            conn.commit()
            self.popup_message.show_message("Changes have been successfully saved.")

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
        self.list_name_input = QLineEdit()
        self.list_name_input.setFixedWidth(300)

    def add_namelist_fields_to_form_layout(self, form_layout):
        form_layout.addRow("Name:", self.list_name_input)

    def populate_namelist_fields_from_db(self):
        conn = self.conn_manager.get_db_connection()
        cursor = conn.cursor()
        cursor = select_from_namelist(cursor, self.nameList_id)
        result = cursor.fetchone()
        if result:
            self.list_name_input.setText(result["listName"])
        conn.close()
