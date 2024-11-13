import logging
from PyQt5.QtWidgets import QFormLayout, QLineEdit, QLabel, QHBoxLayout, QPushButton
from common.connection_manager import ConnectionManager
from database.utils import select_from_description
from gui.common_components.delete_elements import delete_field

class DescriptionForm:
    def __init__(self, communication_id):
        self.communication_id = communication_id
        self.form_layout_right = QFormLayout()
        self.description_ids_to_delete = []
        self.deleted_descriptions_data = []
        self.setup_ui()

    def setup_ui(self):
        self.refresh_ui()

    def refresh_ui(self):
        while self.form_layout_right.rowCount() > 0:
            self.form_layout_right.removeRow(0)

        conn_manager = ConnectionManager()
        conn = conn_manager.get_db_connection()
        cursor = conn.cursor()
        descriptions = select_from_description(cursor, self.communication_id).fetchall()
        conn.close()

        for description in descriptions:
            self.add_descriptions(description)

        logging.debug("Description form refreshed with latest data.")
        return self.form_layout_right

    def add_descriptions(self, description):
        description_label = QLabel("Description")
        description_label.setFixedWidth(80)
        description_input = QLineEdit()
        object_name = f"description_{description['id']}_input"
        description_input.setObjectName(object_name)
        description_input.setFixedSize(550, 30)
        description_input.setText(description['text'] if 'text' in description else "")

        delete_descriptions_button = QPushButton("-")
        delete_descriptions_button.setObjectName("deleteButton")
        delete_descriptions_button.setFixedSize(30, 30)

        hbox_layout = QHBoxLayout()
        hbox_layout.addWidget(description_input)
        hbox_layout.addWidget(delete_descriptions_button)

        self.form_layout_right.addRow(description_label, hbox_layout)

        delete_descriptions_button.clicked.connect(
            lambda: self.delete_description_fields_from_ui(description['id'], description_label, hbox_layout))
        
    def delete_description_fields_from_ui(self, description_id, description_label, hbox_layout):
        delete_field(self.form_layout_right, description_label, hbox_layout)
        self.description_ids_to_delete.append(description_id)
        logging.debug(f"Added description_id {description_id} to delete list. Current list: {self.description_ids_to_delete}")
        #self.refresh_ui()

    def reset_description_fields(self):
        self.description_ids_to_delete.clear()
        self.deleted_descriptions_data.clear()
        self.refresh_ui()
        logging.debug("Reset description form to initial state.")

    def save_descriptions(self):        
        self.description_ids_to_delete.clear()
        self.deleted_descriptions_data.clear()
        self.refresh_ui()
        logging.debug("Descriptions saved and form refreshed.")

    def get_description_ids_to_delete(self):
        logging.debug(f"Returning description_ids_to_delete: {self.description_ids_to_delete}")
        return self.description_ids_to_delete

    def get_form_layout(self):
        return self.form_layout_right
