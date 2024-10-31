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
        self.create_description_form()

    def create_description_form(self):
        conn_manager = ConnectionManager().get_instance()
        conn = conn_manager.get_db_connection()
        cursor = conn.cursor()
        descriptions = select_from_description(cursor, self.communication_id).fetchall()

        for description in descriptions:
            self.add_description_fields(description)

        conn.close()

    def add_description_fields(self, description):
        description_label = QLabel("Description")
        description_label.setFixedWidth(80)
        description_input = QLineEdit()
        object_name = f"description_{description['id']}_input"
        description_input.setObjectName(object_name)
        description_input.setFixedSize(550, 30)

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


    def get_description_ids_to_delete(self):
        logging.debug(f"Returning description_ids_to_delete: {self.description_ids_to_delete}")
        return self.description_ids_to_delete

    def get_form_layout(self):
        return self.form_layout_right