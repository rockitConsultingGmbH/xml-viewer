from PyQt5.QtWidgets import (QVBoxLayout, QFormLayout, QLineEdit, QWidget, QScrollArea, QLabel, QPushButton, 
                             QHBoxLayout, QSpacerItem, QSizePolicy, QGroupBox)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal
from common.connection_manager import ConnectionManager
from database.utils import (select_from_alternatename, select_from_namelist, select_from_namelist_with_communication, update_communication_column, 
                            update_namelist, update_alternatename, insert_into_alternatename, delete_from_alternatename)
from gui.common_components.popup_message import PopupMessage
from gui.common_components.buttons import Buttons
from gui.common_components.stylesheet_loader import load_stylesheet


class NameListsWidget(QWidget):
    name_updated = pyqtSignal(int, str)

    def __init__(self, nameList_id=None, parent=None):
        super().__init__(parent)
        self.nameList_id = str(nameList_id) if nameList_id is not None else ""
        self.conn_manager = ConnectionManager()
        self.popup_message = PopupMessage(self)
        self.entries_to_delete = []
        self.setup_ui()

        load_stylesheet(self, "css/right_widget_styling.qss")

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        layout.addLayout(Buttons().create_button_layout(self))

        self.add_group_box(layout, "Name List", self.create_namelist_layout)

        layout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum))

        self.add_group_box(layout, "Alternate Names", self.create_alternate_names_layout)

        self.setLayout(layout)

    def add_group_box(self, parent_layout, title, content_creator):
        group_box = QGroupBox(title)
        group_box.setObjectName("group-border")
        group_box.setFont(QFont("Arial", 12, QFont.Bold))
        group_box.setStyleSheet("QLabel { border: none; font-size: 12px; } QLineEdit, QCheckBox { font-size: 12px; }")

        group_layout = QVBoxLayout(group_box)
        content_creator(group_layout)
        parent_layout.addWidget(group_box)

    def create_namelist_layout(self, parent_layout):
        namelist_layout = QFormLayout()
        namelist_layout.setSpacing(10)
        self.init_namelist_input_fields()

        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        namelist_layout.addItem(spacer)

        self.communication_label = QLabel("Communication")

        name_layout = QHBoxLayout()
        name_layout.addWidget(self.list_name_input)
        name_layout.addWidget(self.communication_label)

        namelist_layout.addRow("Name:", name_layout)
                            
        self.populate_namelist_fields_from_db()
        parent_layout.addLayout(namelist_layout)

    def create_alternate_names_layout(self, parent_layout):
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        parent_layout.addItem(spacer)

        self.add_new_entry_section(parent_layout)
        self.create_name_entries_layout(parent_layout)

    def add_new_entry_section(self, parent_layout):
        new_entry_layout = QHBoxLayout()

        self.new_entry_input = QLineEdit()
        self.new_entry_input.setFixedWidth(350)
        self.new_entry_input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.new_entry_input.setStyleSheet("padding: 5px; margin: 5px;")
        self.new_entry_input.setPlaceholderText("Enter new entry...")

        add_entry_button = QPushButton("+ Add Entry")
        add_entry_button.setObjectName("addEntryButton")
        add_entry_button.setFixedWidth(100)
        add_entry_button.setFixedHeight(30)
        add_entry_button.clicked.connect(self.add_entry_from_input)

        new_entry_layout.addWidget(self.new_entry_input)
        new_entry_layout.addWidget(add_entry_button)
        new_entry_layout.addStretch()

        parent_layout.addLayout(new_entry_layout)

    def add_entry_from_input(self):
        entry_value = self.new_entry_input.text().strip()

        if entry_value:
            entry_layout = self.create_entry_layout(entry_value)
            self.name_entries_layout.insertLayout(0, entry_layout)
            self.new_entry_input.clear()

    def create_entry_layout(self, entry_value, entry_id=None):
        entry_layout = QHBoxLayout()
        entry_layout.setContentsMargins(0, 0, 0, 0)
        entry_layout.setSpacing(10)

        entry_label = QLabel("Entry:")
        entry_label.setFixedWidth(50)
        entry_label.setAlignment(Qt.AlignLeft)
        entry_layout.addWidget(entry_label)

        entry_input = QLineEdit(entry_value)
        entry_input.setFixedWidth(300)
        entry_input.setFixedHeight(30)
        entry_input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        entry_input.setProperty("entry_id", entry_id)

        delete_button = QPushButton("-")
        delete_button.setObjectName("deleteButton")
        delete_button.setFixedSize(30, 30)
        delete_button.clicked.connect(lambda: self.delete_entry(entry_layout, entry_input))

        entry_layout.addWidget(entry_input)
        entry_layout.addWidget(delete_button)
        entry_layout.setAlignment(Qt.AlignLeft)

        return entry_layout

    def create_name_entries_layout(self, parent_layout):
        entries_widget = QWidget()
        entries_layout = QVBoxLayout(entries_widget)
        entries_layout.setSpacing(10)
        entries_layout.setContentsMargins(10, 10, 10, 10)

        self.name_entries_layout = entries_layout

        name_entries = self.get_name_entries_data()
        for entry in name_entries:
            entry_layout = self.create_entry_layout(entry["entry"], entry["id"])
            self.name_entries_layout.addLayout(entry_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(entries_widget)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.name_entries_layout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))

        parent_layout.addWidget(scroll_area)

    def delete_entry(self, entry_layout, entry_input):
        entry_id = entry_input.property("entry_id")

        if entry_id:  # Only track existing entries for deletion
            self.entries_to_delete.append(entry_id)

        for i in reversed(range(entry_layout.count())):
            widget = entry_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        entry_layout.deleteLater()
        self.name_entries_layout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def save_fields_to_db(self):
        try:
            conn = self.conn_manager.get_db_connection()
            cursor = conn.cursor()

            list_name = self.list_name_input.text()
            communication_id = self.communication_label.property("communication_id")
            print(f"Communication ID: {communication_id}")
            if not list_name:
                self.popup_message.show_error_message("List name cannot be empty.")
                return

            if self.nameList_id:
                row = {"id": self.nameList_id, "listName": list_name}
                update_namelist(cursor, row)
                update_communication_column(cursor, "alternateNameList", list_name, communication_id)
                self.name_updated.emit(int(self.nameList_id), list_name)

            for layout in self.name_entries_layout.children():
                if isinstance(layout, QHBoxLayout):
                    entry_field = layout.itemAt(1).widget()
                    entry_value = entry_field.text()
                    entry_id = entry_field.property("entry_id")
                    row = {"id": entry_id, "nameList_id": self.nameList_id, "entry": entry_value}
                    if entry_value:
                        if entry_id:
                            update_alternatename(cursor, row)
                        else:
                            insert_into_alternatename(cursor, row)

            for entry_id in self.entries_to_delete:
                delete_from_alternatename(cursor, entry_id)

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
        self.clear_name_entries_layout()
        self.reload_name_entries_from_db()

    def clear_name_entries_layout(self):
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

    def reload_name_entries_from_db(self):
        name_entries = self.get_name_entries_data()
        for entry in name_entries:
            entry_layout = self.create_entry_layout(entry["entry"], entry["id"])
            self.name_entries_layout.addLayout(entry_layout)
        self.name_entries_layout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def get_name_entries_data(self):
        try:
            conn = self.conn_manager.get_db_connection()
            cursor = conn.cursor()
            cursor = select_from_alternatename(cursor, self.nameList_id)
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            print(f"Error while fetching name entries data: {e}")
            self.popup_message.show_error_message(f"Error while fetching name entries data: {e}")
            return []
        finally:
            conn.close()

    def init_namelist_input_fields(self):
        self.list_name_input = QLineEdit()
        self.list_name_input.setFixedWidth(300)
        self.list_name_input.setStyleSheet("padding: 5px;")

    def populate_namelist_fields_from_db(self):
        try:
            conn = self.conn_manager.get_db_connection()
            cursor = conn.cursor()

            cursor = select_from_namelist(cursor, self.nameList_id)
            result = cursor.fetchone()
            if result:
                self.list_name_input.setText(result["listName"])

            cursor = select_from_namelist_with_communication(cursor, self.nameList_id)
            result = cursor.fetchone()
            if result:
                self.communication_label.setText(f"Communication: {result['communication_name']}")
                self.communication_label.setProperty("communication_id", result["communication_id"])
        except Exception as e:
            print(f"Error while fetching namelist fields: {e}")
            self.popup_message.show_error_message(f"Error while fetching namelist fields: {e}")
        finally:
            conn.close()
