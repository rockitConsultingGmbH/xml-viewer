import logging
from PyQt5.QtWidgets import QLabel, QCheckBox, QLineEdit, QPushButton, QFormLayout, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QWidget
from common.connection_manager import ConnectionManager
from database.utils import select_from_location
from gui.common_components.clickable_label import ClickableLabel
from gui.common_components.toggle_inputs import toggle_inputs
from controllers.utils.get_and_set_value import set_checkbox_field

class TargetLocationForm:
    def __init__(self, communication_id):
        self.communication_id = communication_id
        self.source_labels = []
        self.source_inputs = []
        self.source_checkboxes = []
        self.target_location_ids_to_delete = []
        self.deleted_target_locations_data = []
        self.target_locations_form_layout = QFormLayout()
        self.conn_manager = ConnectionManager()
        self.load_target_locations()

    def load_target_locations(self):
        self.conn = self.conn_manager.get_db_connection()
        self.cursor = self.conn.cursor()
        self.target_locations = [dict(row) for row in select_from_location(self.cursor, self.communication_id, 'targetLocation').fetchall()]
        self.conn.close()

    def setup_ui(self):
        self.load_target_locations()
        for target_location in self.target_locations:
            self.add_target_location_fields(target_location)
        return self.target_locations_form_layout

    def add_target_location_fields(self, target_location):
        logging.info(f"Adding target location fields for targetLocation ID: {target_location['id']}")
        
        target_box_widget = QWidget()
        target_box_widget.setObjectName(f"target_box_{target_location['id']}")
        target_box_widget.setProperty("target_id", target_location['id'])

        target_box = QVBoxLayout(target_box_widget)
        target_label = ClickableLabel("Target")
        target_label.setFixedWidth(80)
        target_label.setStyleSheet("font-weight: bold;")
        self.target_input = QLineEdit()
        self.target_input.setFixedHeight(30)
        self.target_input.setObjectName(f"target_{target_location['id']}_input")

        target_delete_button = QPushButton("-")
        target_delete_button.setObjectName("deleteButton")
        target_delete_button.setFixedSize(30, 30)

        target_row_layout = QHBoxLayout()
        target_row_layout.addWidget(target_label)
        target_row_layout.addWidget(self.target_input)
        target_row_layout.addWidget(target_delete_button)

        upper_layout = QFormLayout()
        upper_layout.addRow(target_row_layout)
        upper_layout.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))
        target_box.addLayout(upper_layout)

        hbox_columns = QHBoxLayout()
        left_column_layout = QFormLayout()
        right_column_layout = QFormLayout()

        userid_label = QLabel("User ID")
        self.userid_input = QLineEdit()
        self.userid_input.setObjectName(f"userid_target_{target_location['id']}_input")
        self.userid_input.setFixedHeight(30)

        password_label = QLabel("Password")
        self.password_input = QLineEdit()
        self.password_input.setObjectName(f"password_target_{target_location['id']}_input")
        self.password_input.setFixedHeight(30)

        location_id_label = QLabel("Location ID")
        self.location_id_input = QLineEdit()
        self.location_id_input.setObjectName(f"location_id_target_{target_location['id']}_input")
        self.location_id_input.setFixedHeight(30)

        target_description_label = QLabel("Description")
        self.target_description_input = QLineEdit()
        self.target_description_input.setObjectName(f"target_description_{target_location['id']}_input")
        self.target_description_input.setFixedHeight(30)

        left_column_layout.addRow(userid_label, self.userid_input)
        right_column_layout.addRow(password_label, self.password_input)
        left_column_layout.addRow(location_id_label, self.location_id_input)
        right_column_layout.addRow(target_description_label, self.target_description_input)

        # Checkboxes
        self.use_local_filename_checkbox = QCheckBox("Use Local Filename")
        self.use_local_filename_checkbox.setObjectName(f"use_local_filename_checkbox_target_{target_location['id']}")

        self.use_path_from_config_checkbox = QCheckBox("Use Path From Config")
        self.use_path_from_config_checkbox.setObjectName(f"use_path_from_config_checkbox_target_{target_location['id']}")

        self.rename_existing_file_checkbox = QCheckBox("Rename Existing File")
        self.rename_existing_file_checkbox.setObjectName(f"rename_existing_file_checkbox_{target_location['id']}")

        # Checkbox layout
        checkbox_layout = QHBoxLayout()
        checkbox_layout.addWidget(self.use_local_filename_checkbox)
        checkbox_layout.addWidget(self.use_path_from_config_checkbox)
        checkbox_layout.addWidget(self.rename_existing_file_checkbox)
        left_column_layout.addRow(checkbox_layout)

        left_column_with_margin = QHBoxLayout()
        left_margin = QSpacerItem(90, 0, QSizePolicy.Fixed, QSizePolicy.Minimum)
        left_column_with_margin.addItem(left_margin)
        left_column_with_margin.addLayout(left_column_layout)

        hbox_columns.addLayout(left_column_with_margin)
        hbox_columns.addSpacing(50)
        hbox_columns.addLayout(right_column_layout)

        target_box.addLayout(hbox_columns)
        target_box.addItem(QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))
        self.target_locations_form_layout.addRow(target_box_widget)

        target_delete_button.clicked.connect(lambda: self.mark_target_location_for_deletion(target_location['id'], target_box_widget, target_location))
        self.populate_target_fields(target_location, target_box_widget)

        # Extend lists to be toggled
        self.source_labels.extend([userid_label, location_id_label, password_label, target_description_label])
        self.source_inputs.extend([self.userid_input, self.location_id_input, self.password_input, self.target_description_input])
        self.source_checkboxes.extend([self.use_local_filename_checkbox, self.use_path_from_config_checkbox, self.rename_existing_file_checkbox])

        target_label.mousePressEvent = lambda event: toggle_inputs(self.source_labels + self.source_checkboxes, self.source_inputs)

    def populate_target_fields(self, target_location, parent_widget):
        self.target_input.setText(target_location["location"])
        self.userid_input.setText(target_location["userid"])
        self.password_input.setText(target_location["password"])
        self.location_id_input.setText(target_location["location_id"])
        self.target_description_input.setText(target_location["description"])
        
        set_checkbox_field(parent_widget, f"use_local_filename_checkbox_target_{target_location['id']}", target_location["useLocalFilename"])
        set_checkbox_field(parent_widget, f"use_path_from_config_checkbox_target_{target_location['id']}", target_location["usePathFromConfig"])
        set_checkbox_field(parent_widget, f"rename_existing_file_checkbox_{target_location['id']}", target_location["renameExistingFile"])

    def mark_target_location_for_deletion(self, target_location_id, target_box_widget, target_location):
        if target_location_id == 'new':
            target_box_widget.setVisible(False)
            return
        self.target_location_ids_to_delete.append(target_location_id)
        self.deleted_target_locations_data.append(target_location)
        target_box_widget.setVisible(False)
        logging.debug(f"Marked targetLocation_id {target_location_id} for deletion.")

    def reset_target_location_deletions(self):
        self.target_location_ids_to_delete.clear()
        self.deleted_target_locations_data.clear()
        self.refresh_form()
        logging.debug("Reset target location deletions and refreshed the form.")

    def refresh_form(self):
        while self.target_locations_form_layout.count():
            item = self.target_locations_form_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())
        self.load_target_locations()
        self.setup_ui()
        logging.debug("Refreshed target locations form layout.")

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

    def get_target_location_ids_to_delete(self):
        logging.debug(f"Returning location_ids_to_delete: {self.target_location_ids_to_delete}")
        return self.target_location_ids_to_delete
