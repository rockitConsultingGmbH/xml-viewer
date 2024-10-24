from PyQt5.QtWidgets import QFormLayout, QLineEdit, QLabel

from common.connection_manager import ConnectionManager
from database.utils import select_from_description

class DescriptionForm:
    def __init__(self, communication_id):
        self.communication_id = communication_id
        self.form_layout_right = QFormLayout()
        #self.input_names = []
        self.create_description_form()

    def create_description_form(self):
        conn_manager = ConnectionManager().get_instance()
        conn = conn_manager.get_db_connection()
        cursor = conn.cursor()
        descriptions = select_from_description(cursor, self.communication_id)

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

        self.form_layout_right.addRow(description_label, description_input)
        #self.input_names.append(object_name)

    def get_form_layout(self):
        return self.form_layout_right
