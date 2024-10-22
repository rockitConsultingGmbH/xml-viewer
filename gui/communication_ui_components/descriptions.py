from PyQt5.QtWidgets import QFormLayout, QLineEdit, QLabel

from common.connection_manager import ConnectionManager
from database.utils import select_from_description

input_names = []

def create_description_form(label_style, communication_id):
    form_layout_right = QFormLayout()

    conn_manager = ConnectionManager().get_instance()
    conn = conn_manager.get_db_connection()
    cursor = conn.cursor()
    descriptions = select_from_description(cursor, communication_id)

    for description in descriptions:
        add_description_fields(form_layout_right, label_style, description)

    conn.close()
    return form_layout_right

def add_description_fields(form_layout_right, label_style, description):
    description_label = QLabel("Description")
    description_label.setStyleSheet(label_style)
    description_input = QLineEdit(description["description"])
    object_name = f"description_{description['id']}_input"
    description_input.setObjectName(object_name)
    description_input.setFixedSize(550, 30)

    form_layout_right.addRow(description_label, description_input)
    input_names.append(object_name)