import logging
from PyQt5.QtWidgets import QFormLayout, QLineEdit, QLabel, QCheckBox, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QWidget, QPushButton

from common.connection_manager import ConnectionManager
from database.utils import select_from_location

from gui.common_components.clickable_label import ClickableLabel


class TargetLocationForm:
    def __init__(self, communication_id):
        self.communication_id = communication_id
        self.target_location_ids_to_delete = []
        self.deleted_target_locations_data = []
        self.target_locations_form_layout = QFormLayout()
        self.conn_manager = ConnectionManager()
        self.load_target_locations()

    def load_target_locations(self):
        self.conn = self.conn_manager.get_db_connection()
        self.cursor = self.conn.cursor()
        self.targetLocations = [dict(row) for row in select_from_location(self.cursor, self.communication_id, 'targetLocation').fetchall()]
        self.conn.close()

    def create_form(self):
        for targetLocation in self.targetLocations:
            self.add_target_location_fields(targetLocation)
        return self.target_locations_form_layout

    def add_target_location_fields(self, targetLocation):
        logging.info(f"Adding target location fields for targetLocation ID: {targetLocation['id']}")
        
        target_box_widget = QWidget()
        target_box_widget.setObjectName(f"target_box_{targetLocation['id']}")
        target_box_widget.setProperty("target_id", targetLocation['id'])

        target_box = QVBoxLayout(target_box_widget)
        target_label = ClickableLabel("Target")
        target_label.setFixedWidth(80)
        target_label.setStyleSheet("font-weight: bold;")
        target_input = QLineEdit()
        target_input.setFixedHeight(30)
        target_input.setObjectName(f"target_{targetLocation['id']}_input")
        target_input.setText(targetLocation['location'])

        target_delete_button = QPushButton("-")
        target_delete_button.setObjectName("deleteButton")
        target_delete_button.setFixedSize(30, 30)

        target_row_layout = QHBoxLayout()
        target_row_layout.addWidget(target_label)
        target_row_layout.addWidget(target_input)
        target_row_layout.addWidget(target_delete_button)

        upper_layout = QFormLayout()
        upper_layout.addRow(target_row_layout)
        upper_layout.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))

        target_box.addLayout(upper_layout)

        hbox_columns = QHBoxLayout()
        left_column_layout = QFormLayout()
        right_column_layout = QFormLayout()
    
        userid_input = QLineEdit()
        userid_input.setObjectName(f"userid_target_{targetLocation['id']}_input")
        userid_input.setFixedHeight(30)
        userid_input.setText(targetLocation['userid'])

        password_input = QLineEdit()
        password_input.setObjectName(f"password_target_{targetLocation['id']}_input")
        password_input.setFixedHeight(30)
        password_input.setText(targetLocation['password'])

        location_id_input = QLineEdit()
        location_id_input.setObjectName(f"location_id_target_{targetLocation['id']}_input")
        location_id_input.setFixedHeight(30)
        location_id_input.setText(targetLocation['location_id'])

        target_description_input = QLineEdit()
        target_description_input.setObjectName(f"target_description_{targetLocation['id']}_input")
        target_description_input.setFixedHeight(30)
        target_description_input.setText(targetLocation['description'])

        left_column_layout.addRow(QLabel("User ID"), userid_input)
        right_column_layout.addRow(QLabel("Password"), password_input)
        left_column_layout.addRow(QLabel("Location ID"), location_id_input)
        right_column_layout.addRow(QLabel("Description"), target_description_input)

        use_local_filename_checkbox = QCheckBox("Use Local Filename")
        use_local_filename_checkbox.setObjectName(f"use_local_filename_target_{targetLocation['id']}_checkbox")
        use_local_filename_checkbox.setChecked(bool(targetLocation['useLocalFilename']))

        use_path_from_config_checkbox = QCheckBox("Use Path From Config")
        use_path_from_config_checkbox.setObjectName(f"use_path_from_config_target_{targetLocation['id']}_checkbox")
        use_path_from_config_checkbox.setChecked(bool(targetLocation['usePathFromConfig']))

        rename_existing_file_checkbox = QCheckBox("Rename Existing File")
        rename_existing_file_checkbox.setObjectName(f"rename_existing_file_target_{targetLocation['id']}_checkbox")
        rename_existing_file_checkbox.setChecked(bool(targetLocation['renameExistingFile']))

        checkbox_layout = QHBoxLayout()
        checkbox_layout.addWidget(use_local_filename_checkbox)
        checkbox_layout.addWidget(use_path_from_config_checkbox)
        checkbox_layout.addWidget(rename_existing_file_checkbox)
        left_column_layout.addRow(checkbox_layout)

        left_column_with_margin = QHBoxLayout()
        left_column_with_margin.addItem(QSpacerItem(90, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))
        left_column_with_margin.addLayout(left_column_layout)

        hbox_columns.addLayout(left_column_with_margin)
        hbox_columns.addSpacing(50)
        hbox_columns.addLayout(right_column_layout)

        target_box.addLayout(hbox_columns)

        self.target_locations_form_layout.addRow(target_box_widget)
        self.target_locations_form_layout.addItem(QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        target_delete_button.clicked.connect(lambda: self.mark_target_location_for_deletion(targetLocation['id'], target_box_widget, targetLocation))

    def mark_target_location_for_deletion(self, targetLocation_id, target_box_widget, targetLocation):
        self.target_location_ids_to_delete.append(targetLocation_id)
        self.deleted_target_locations_data.append(targetLocation)
        target_box_widget.setVisible(False)
        logging.debug(f"Marked targetLocation_id {targetLocation_id} for deletion.")

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
        self.create_form()
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
