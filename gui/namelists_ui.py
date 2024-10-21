from PyQt5.QtWidgets import (QVBoxLayout, QFormLayout, QLineEdit, QWidget, QScrollArea, QLabel, QFrame, QPushButton, 
                             QHBoxLayout, QSpacerItem, QSizePolicy, QGroupBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal
from common.connection_manager import ConnectionManager
from database.utils import select_from_alternatename, select_from_namelist_with_communication, update_communication_column, update_namelist, update_alternatename, insert_into_alternatename, delete_from_alternatename
from gui.components.popup_message_ui import PopupMessage
from gui.components.buttons import ButtonFactory
from common.config_manager import config_manager

class NameListsWidget(QWidget):
    name_updated = pyqtSignal(int, str)

    def __init__(self, nameList_id=None, parent=None):
        super().__init__(parent)
        self.nameList_id = str(nameList_id) if nameList_id is not None else ""
        self.conn_manager = ConnectionManager.get_instance()
        self.popup_message = PopupMessage(self)
        self.entries_to_delete = []  # Track entries marked for deletion
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # Add Save and Reset buttons
        layout.addLayout(ButtonFactory().create_button_layout(self))

        # Add the Name List group box
        name_list_group_box = QGroupBox("Name List")
        name_list_group_box.setFont(QFont("Arial", 10, QFont.Bold))
        name_list_layout = QVBoxLayout(name_list_group_box)
        self.create_namelist_layout(name_list_layout)
        layout.addWidget(name_list_group_box)

        # Add vertical spacing before the "Alternate Names" group box
        layout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum))

        # Add the Alternate Names group box
        alternate_names_group_box = QGroupBox("Alternate Names")
        alternate_names_group_box.setFont(QFont("Arial", 10, QFont.Bold))
        alternate_names_layout = QVBoxLayout(alternate_names_group_box)
        self.add_new_entry_section(alternate_names_layout)
        self.create_name_entries_layout(alternate_names_layout)
        layout.addWidget(alternate_names_group_box)

        self.setLayout(layout)

    def create_namelist_layout(self, parent_layout):
        namelist_layout = QFormLayout()
        namelist_layout.setSpacing(10)
        self.init_namelist_input_fields()

        # Create clickable communication name label
        self.communication_label = QLabel("Communication")

        # Add the Name field and Communication label in a horizontal layout
        name_layout = QHBoxLayout()
        name_layout.addWidget(self.list_name_input)
        name_layout.addWidget(self.communication_label)

        # Add the horizontal layout to the form layout
        namelist_layout.addRow("Name:", name_layout)
                            
        self.populate_namelist_fields_from_db()
        parent_layout.addLayout(namelist_layout)

    def add_new_entry_section(self, parent_layout):
        # Create layout for entry input and button
        new_entry_layout = QHBoxLayout()

        # Create input field for adding new entry
        self.new_entry_input = QLineEdit()
        self.new_entry_input.setFixedWidth(350)
        self.new_entry_input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.new_entry_input.setStyleSheet("padding: 5px; margin: 5px;")
        self.new_entry_input.setPlaceholderText("Enter new entry...")

        # Create "Add Entry" button
        add_entry_button = QPushButton("+ Add Entry")
        add_entry_button.setFixedWidth(100)
        add_entry_button.setFixedHeight(30)
        add_entry_button.clicked.connect(self.add_entry_from_input)

        # Align the input field and button to the left
        new_entry_layout.addWidget(self.new_entry_input)
        new_entry_layout.addWidget(add_entry_button)
        new_entry_layout.addStretch()

        parent_layout.addLayout(new_entry_layout)

    def add_entry_from_input(self):
        entry_value = self.new_entry_input.text().strip()

        if entry_value:
            entry_layout = QHBoxLayout()
            entry_layout.setContentsMargins(0, 0, 0, 0)
            entry_layout.setSpacing(10)

            # Create a QLabel for "Entry:"
            entry_label = QLabel("Entry:")
            entry_label.setFixedWidth(50)
            entry_label.setAlignment(Qt.AlignLeft)
            entry_layout.addWidget(entry_label)

            # Create a QLineEdit for the new entry
            entry_input = QLineEdit(entry_value)
            entry_input.setFixedWidth(300)
            entry_input.setFixedHeight(30)
            entry_input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            entry_input.setProperty("entry_id", None)

            # Add delete button (a minus sign) to remove the entry
            delete_button = QPushButton("x")
            delete_button.setFixedSize(30, 30)
            delete_button.clicked.connect(lambda: self.delete_entry(entry_layout, entry_input))

            # Add the widgets
            entry_layout.addWidget(entry_input)
            entry_layout.addWidget(delete_button)
            entry_layout.setAlignment(Qt.AlignLeft)

            # Insert the new entry layout at the top of the entries
            self.name_entries_layout.insertLayout(0, entry_layout)

            # Clear the input field after adding the entry
            self.new_entry_input.clear()

    def create_name_entries_layout(self, parent_layout):
        entries_widget = QWidget()
        entries_layout = QVBoxLayout(entries_widget)
        entries_layout.setSpacing(10)
        entries_layout.setContentsMargins(10, 10, 10, 10)

        self.name_entries_layout = entries_layout

        # Load existing entries from the database
        name_entries = self.get_name_entries_data()
        for entry in name_entries:
            entry_layout = QHBoxLayout()
            self.add_name_entries_fields_to_form_layout(entry_layout, entry)
            self.name_entries_layout.addLayout(entry_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(entries_widget)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.name_entries_layout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Add scroll area to the parent layout
        parent_layout.addWidget(scroll_area)

    def add_name_entries_fields_to_form_layout(self, entry_layout, entry):
        entry_label = QLabel("Entry:")
        entry_label.setFixedWidth(50)
        entry_layout.addWidget(entry_label)

        entry_input = QLineEdit(entry["entry"])
        entry_input.setFixedWidth(300)
        entry_input.setFixedHeight(30)
        entry_input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Store the entry ID in the QLineEdit's properties
        entry_input.setProperty("entry_id", entry["id"])

        # Add delete button (a minus sign) to remove the entry
        delete_button = QPushButton("x")
        delete_button.setFixedSize(30, 30)
        delete_button.clicked.connect(lambda: self.delete_entry(entry_layout, entry_input))

        entry_layout.addWidget(entry_input)
        entry_layout.addWidget(delete_button)
        entry_layout.setAlignment(Qt.AlignLeft)

    def delete_entry(self, entry_layout, entry_input):
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
        self.name_entries_layout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def save_fields_to_db(self):
        try:
            conn = self.conn_manager.get_db_connection()
            cursor = conn.cursor()

            # Save or update the NameList table
            list_name = self.list_name_input.text()
            communication_id = self.communication_label.property("communication_id")
            if not list_name:
                self.popup_message.show_error_message("List name cannot be empty.")
                return

            if self.nameList_id:
                # Update existing NameList if nameList_id is present
                row = {
                    "id": self.nameList_id,
                    "listName": list_name
                }
                update_namelist(cursor, row)
                #update_communication_column(cursor, 'alternateNameList', list_name, communication_id, config_manager.config_id)

                # Emit the name_updated signal to notify MainWindow
                self.name_updated.emit(int(self.nameList_id), list_name)

            # Save or update the AlternateName table for each entry
            for layout in self.name_entries_layout.children():
                if isinstance(layout, QHBoxLayout):
                    entry_field = layout.itemAt(1).widget()
                    entry_value = entry_field.text()

                    # Retrieve the entry ID from the field's property
                    entry_id = entry_field.property("entry_id")
                    row = {
                        "id": entry_id,
                        "nameList_id": self.nameList_id,
                        "entry": entry_value
                    }
                    if entry_value:
                        if entry_id:
                            update_alternatename(cursor, row)
                        else:
                            # Entry doesn't exist, insert new
                            insert_into_alternatename(cursor, row)

            # Process entries marked for deletion
            if self.entries_to_delete:
                for entry_id in self.entries_to_delete:
                    delete_from_alternatename(cursor, entry_id)

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
        self.populate_namelist_fields_from_db()

        # Clear the current entries layout
        for i in reversed(range(self.name_entries_layout.count())):
            layout_item = self.name_entries_layout.itemAt(i)
            if isinstance(layout_item, QHBoxLayout):
                for j in reversed(range(layout_item.count())):
                    widget = layout_item.itemAt(j).widget()
                    if widget:
                        widget.deleteLater()
                layout_item.deleteLater()
            elif isinstance(layout_item, QSpacerItem):
                self.name_entries_layout.removeItem(layout_item)

        # Reload the AlternateName entries from the database
        name_entries = self.get_name_entries_data()
        for entry in name_entries:
            entry_layout = QHBoxLayout()
            self.add_name_entries_fields_to_form_layout(entry_layout, entry)
            self.name_entries_layout.addLayout(entry_layout)

        # Add the spacer item after all entries have been added
        self.name_entries_layout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))

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
        self.list_name_input.setStyleSheet("padding: 5px;")

    def add_namelist_fields_to_form_layout(self, form_layout):
        form_layout.addRow("Name:", self.list_name_input)

    def populate_namelist_fields_from_db(self):
        conn = self.conn_manager.get_db_connection()
        cursor = conn.cursor()

        # Fetch NameList information based on nameList_id
        cursor = select_from_namelist_with_communication(cursor, self.nameList_id)
        result = cursor.fetchone()
        
        if result:
            # Populate the Name field
            self.list_name_input.setText(result["listName"])

            # Set the communication label text to the communication name
            self.communication_label.setText(f"Communication: {result['communication_name']}")
            # Optionally set the communication ID to the label's property if needed for further interaction
            self.communication_label.setProperty("communication_id", result["communication_id"])
        conn.close()
