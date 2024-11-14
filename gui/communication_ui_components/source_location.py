import logging
from PyQt5.QtWidgets import QLabel, QLineEdit, QFormLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QVBoxLayout, QWidget
from gui.common_components.clickable_label import ClickableLabel
from common.connection_manager import ConnectionManager
from database.utils import select_from_location
from gui.common_components.toggle_inputs import toggle_inputs

class SourceLocationForm(QWidget):
    def __init__(self, communication_id, parent_widget=None):
        super().__init__()
        self.parent_widget = parent_widget
        self.communication_id = communication_id
        self.toggle_inputs = toggle_inputs
        self.source_labels = []
        self.source_inputs = []
        self.source_checkboxes = []
        self.source_locations_form_layout = QFormLayout()
        self.conn_manager = ConnectionManager()

    def load_source_locations(self):
        self.conn = self.conn_manager.get_db_connection()
        self.cursor = self.conn.cursor()
        self.source_locations = [dict(row) for row in select_from_location(self.cursor, self.communication_id, 'sourceLocation').fetchall()]
        self.conn.close()

    def setup_ui(self):
        self.load_source_locations()

        self.source_locations_form_layout.setHorizontalSpacing(20)
        self.source_locations_form_layout.setVerticalSpacing(15)

        for source_location in self.source_locations:
            self.add_source_location_fields(source_location)
        return self.source_locations_form_layout

    def add_source_location_fields(self, source_location):
        source_label = ClickableLabel("Source")
        source_label.setFixedWidth(70)
        source_label.setStyleSheet("font-weight: bold;")
        self.source_input = QLineEdit()
        self.source_input.setFixedHeight(30)
        self.source_input.setObjectName("source_input")
        
        self.source_locations_form_layout.addRow(source_label, self.source_input)

        hbox_columns = QHBoxLayout()
        left_column_layout = QFormLayout()
        left_column_layout.setVerticalSpacing(15)

        userid_label = QLabel("User ID")
        self.userid_input = QLineEdit()
        self.userid_input.setObjectName("userid_source_input")
        self.userid_input.setFixedHeight(30)
        left_column_layout.addRow(userid_label, self.userid_input)

        location_id_label = QLabel("Location ID")
        location_id_label.setFixedWidth(100)
        self.location_id_input = QLineEdit()
        self.location_id_input.setObjectName("location_id_input")
        self.location_id_input.setFixedHeight(30)
        left_column_layout.addRow(location_id_label, self.location_id_input)

        right_column_layout = QFormLayout()
        right_column_layout.setVerticalSpacing(15)

        password_label = QLabel("Password")
        password_label.setFixedWidth(80)
        self.password_input = QLineEdit()
        self.password_input.setObjectName("password_source_input")
        self.password_input.setFixedHeight(30)
        right_column_layout.addRow(password_label, self.password_input)

        source_description_label = QLabel("Description")
        source_description_label.setFixedWidth(100)
        self.source_description_input = QLineEdit()
        self.source_description_input.setObjectName("source_description_input")
        self.source_description_input.setFixedHeight(30)
        right_column_layout.addRow(source_description_label, self.source_description_input)

        left_column_with_margin = QHBoxLayout()
        left_margin = QSpacerItem(90, 0, QSizePolicy.Fixed, QSizePolicy.Minimum)
        left_column_with_margin.addItem(left_margin)
        left_column_with_margin.addLayout(left_column_layout)

        hbox_columns.addLayout(left_column_with_margin)
        hbox_columns.addSpacing(50)
        hbox_columns.addLayout(right_column_layout)

        self.source_locations_form_layout.addRow(hbox_columns)

        self.source_labels.extend([userid_label, location_id_label, password_label, source_description_label])
        self.source_inputs.extend([self.userid_input, self.location_id_input, self.password_input, self.source_description_input])
        source_label.mousePressEvent = lambda event: self.toggle_inputs(self.source_labels, self.source_inputs)

        self.populate_fields(source_location)

    def populate_fields(self, data):
        self.source_input.setText(data["location"])
        self.userid_input.setText(data["userid"])
        self.location_id_input.setText(data["location_id"])
        self.password_input.setText(data["password"])
        self.source_description_input.setText(data["description"])

    def reset_source_location(self):
        self.load_source_locations()
        self.refresh_form()
        logging.debug("Reset source location fields and refreshed the form.")

    def refresh_form(self):
        while self.source_locations_form_layout.count():
            item = self.source_locations_form_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

        self.setup_ui()
        logging.debug("Refreshed source location form layout with latest data.")

    def clear_layout(self, layout):
        """Recursively clear all items in a layout."""
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())
