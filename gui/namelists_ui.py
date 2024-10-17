from PyQt5.QtWidgets import (QVBoxLayout, QFormLayout, QLineEdit, QWidget, QScrollArea, QLabel, QFrame, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy)
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

        # Add Save and Reset buttons above the "Name List" divider
        layout.addLayout(ButtonFactory().create_button_layout(self))

        # Add a divider for "Name List"
        self.add_divider(layout, "Name List")

        self.create_namelist_layout(layout)

        # Add vertical spacing before the "Alternate Names" divider
        spacer = QSpacerItem(20, 10, QSizePolicy.Minimum)
        layout.addItem(spacer)  # Add the spacer to the layout

        # Add a divider for "Alternate Names"
        self.add_divider(layout, "Alternate Names")

        # Add button to create a new entry after the "Alternate Names" divider
        self.add_new_entry_section(layout)

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
        label.setAlignment(Qt.AlignLeft)  # Align the divider label to the left

        layout.addWidget(label)
        layout.addWidget(divider)

    def add_new_entry_section(self, parent_layout):
        # Create layout for entry input and button
        new_entry_layout = QHBoxLayout()

        # Create input field for adding new entry
        self.new_entry_input = QLineEdit()
        self.new_entry_input.setFixedWidth(350)  # Set the width to match Name field
        self.new_entry_input.setStyleSheet("padding: 5px; margin: 5px;")  # Add consistent padding and margin
        self.new_entry_input.setPlaceholderText("Enter new entry...")

        # Create "Add Entry" button
        add_entry_button = QPushButton("+ Add Entry")
        add_entry_button.setFixedWidth(100)  # Set the button width
        add_entry_button.clicked.connect(self.add_entry_from_input)

        # Align the input field and button to the left
        new_entry_layout.addWidget(self.new_entry_input)
        new_entry_layout.addWidget(add_entry_button)
        new_entry_layout.addStretch()  # Add stretch to push everything to the left

        parent_layout.addLayout(new_entry_layout)

    def add_entry_from_input(self):
        """Insert a new entry at the top when the user clicks 'Add Entry'."""
        entry_value = self.new_entry_input.text().strip()

        if entry_value:
            entry_layout = QHBoxLayout()

            # Create a QLineEdit for the new entry
            entry_input = QLineEdit(entry_value)
            entry_input.setFixedWidth(300)  # Set a fixed width for consistent layout
            entry_input.setStyleSheet("padding: 5px;")
            entry_input.setProperty("entry_id", None)  # This is a new entry with no ID yet

            # Add delete button (a minus sign) to remove the entry
            delete_button = QPushButton("x")
            delete_button.setFixedSize(30, 30)
            delete_button.clicked.connect(lambda: self.delete_entry(entry_layout, entry_input))

            # Add the widgets
            entry_layout.addWidget(QLabel("Entry:"))
            entry_layout.addWidget(entry_input, stretch=1)
            entry_layout.addWidget(delete_button, alignment=Qt.AlignRight)

            # Insert the new entry layout at the top of the entries
            self.name_entries_layout.insertLayout(0, entry_layout)

            # Clear the input field after adding the entry
            self.new_entry_input.clear()

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
        entry_input.setStyleSheet("padding: 5px; margin: 5px;")  # Add consistent padding and margin

        # Store the entry ID in the QLineEdit's properties
        entry_input.setProperty("entry_id", entry["id"])

        # Add delete button (a minus sign) to remove the entry
        delete_button = QPushButton("x")
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

        # Add a spacer item to maintain consistent spacing
        spacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.name_entries_layout.addItem(spacer)

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
        self.list_name_input.setFixedWidth(300)  # Set the width to match the entry fields

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
