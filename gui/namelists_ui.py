from PyQt5.QtWidgets import (QVBoxLayout, QFormLayout, QLineEdit, QWidget, QScrollArea, QLabel, QFrame, QPushButton, QHBoxLayout)
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
        self.entries_to_delete = []  # Track entries marked for deletion
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Add button to create a new entry (top left)
        self.add_new_entry_button(layout)

        layout.addLayout(ButtonFactory().create_button_layout(self))
        self.create_namelist_layout(layout)
        self.add_divider(layout, "Alternate Names")

        # Create the alternate name entries section
        self.create_name_entries_layout(layout)
        self.setLayout(layout)

    def create_namelist_layout(self, parent_layout):
        namelist_layout = QFormLayout()
        namelist_layout.setSpacing(10)
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

    def add_new_entry_button(self, parent_layout):
        add_entry_button = QPushButton("+ Add Entry")
        add_entry_button.setFixedWidth(100)  # Set the button width
        add_entry_button.clicked.connect(self.add_empty_entry)
        
        # Align button to the left
        button_layout = QHBoxLayout()
        button_layout.addWidget(add_entry_button)
        button_layout.setAlignment(Qt.AlignLeft)  # Align to left
        
        parent_layout.addLayout(button_layout)  # Add the button layout to the top

    def add_empty_entry(self):
        entry_layout = QHBoxLayout()

        # Create a QLineEdit for the new entry
        entry_input = QLineEdit()
        entry_input.setFixedWidth(300)  # Set a fixed width for consistent layout

        # Set a custom property to indicate this is a new entry (no ID yet)
        entry_input.setProperty("entry_id", None)

        # Add delete button (a minus sign) to remove the entry
        delete_button = QPushButton("-")
        delete_button.setFixedSize(30, 30)
        delete_button.clicked.connect(lambda: self.delete_entry(entry_layout, entry_input))

        # Add the widgets and a stretch for proper alignment and spacing
        entry_layout.addWidget(QLabel("Entry:"))
        entry_layout.addWidget(entry_input, stretch=1)  # Stretch to allow the input to take up space
        entry_layout.addWidget(delete_button, alignment=Qt.AlignRight)

        # Add the new entry layout to the main layout
        self.name_entries_layout.addLayout(entry_layout)

    def create_name_entries_layout(self, parent_layout):
        entries_widget = QWidget()
        self.name_entries_layout = QVBoxLayout(entries_widget)
        self.name_entries_layout.setSpacing(10)
        self.name_entries_layout.setContentsMargins(10, 10, 10, 10)

        # Load existing entries from the database
        name_entries = self.get_name_entries_data()
        for entry in name_entries:
            entry_layout = QHBoxLayout()
            self.add_name_entries_fields_to_form_layout(entry_layout, entry)
            self.name_entries_layout.addLayout(entry_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidget(entries_widget)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        parent_layout.addWidget(scroll_area)

    def add_name_entries_fields_to_form_layout(self, entry_layout, entry):
        entry_label = QLabel("Entry:")
        entry_input = QLineEdit(entry["entry"])
        entry_input.setFixedWidth(300)

        # Store the entry ID in the QLineEdit's properties
        entry_input.setProperty("entry_id", entry["id"])

        # Add delete button (a minus sign) to remove the entry
        delete_button = QPushButton("-")
        delete_button.setFixedSize(30, 30)
        delete_button.clicked.connect(lambda: self.delete_entry(entry_layout, entry_input))

        entry_layout.addWidget(entry_label)
        entry_layout.addWidget(entry_input)
        entry_layout.addWidget(delete_button)

    def delete_entry(self, entry_layout, entry_input):
        """Visually remove the entry from the UI and mark it for deletion."""
        entry_id = entry_input.property("entry_id")

        if entry_id:  # Only track existing entries for deletion
            self.entries_to_delete.append(entry_id)

        # Remove the layout from the UI
        for i in reversed(range(entry_layout.count())):
            widget = entry_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        entry_layout.deleteLater()

    def save_fields_to_db(self):
        """Save or update entries in the database, including deletion of marked entries."""
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
                if isinstance(layout, QHBoxLayout):
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

            # Process entries marked for deletion
            if self.entries_to_delete:
                cursor.executemany("""
                    DELETE FROM AlternateName 
                    WHERE id = ?
                """, [(entry_id,) for entry_id in self.entries_to_delete])

            # Clear the deletion list after committing changes
            self.entries_to_delete = []

            conn.commit()
            self.popup_message.show_message("Changes have been successfully saved.")

        except Exception as e:
            print(f"Error while saving data: {e}")
            conn.rollback()
            self.popup_message.show_error_message(f"Error while saving data: {e}")
        finally:
            conn.close()

    def set_fields_from_db(self):
        """Reset the fields to the original values from the database."""
        self.populate_namelist_fields_from_db()  # Reset the NameList fields

        # Clear the current entries layout
        for i in reversed(range(self.name_entries_layout.count())):
            layout_item = self.name_entries_layout.itemAt(i)
            if isinstance(layout_item, QHBoxLayout):
                for j in reversed(range(layout_item.count())):
                    widget = layout_item.itemAt(j).widget()
                    if widget:
                        widget.deleteLater()
                layout_item.deleteLater()

        # Reload the AlternateName entries from the database
        name_entries = self.get_name_entries_data()
        for entry in name_entries:
            entry_layout = QHBoxLayout()
            self.add_name_entries_fields_to_form_layout(entry_layout, entry)
            self.name_entries_layout.addLayout(entry_layout)

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
