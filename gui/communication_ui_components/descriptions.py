from PyQt5.QtWidgets import QFormLayout, QLineEdit, QLabel

from common.connection_manager import ConnectionManager
from database.utils import select_from_description
from utils.clickable_label import ClickableLabel

input_names = []


def create_description_form(label_style, communication_id):
    form_layout_right = QFormLayout()
    description_label = ClickableLabel("Description(s)")
    description_label.setStyleSheet(label_style)

    conn_manager = ConnectionManager().get_instance()
    conn = conn_manager.get_db_connection()
    cursor = conn.cursor()
    descriptions = select_from_description(cursor, communication_id)

    for description in descriptions:
        description_label = QLabel(description["descriptionType"])
        description_input = QLineEdit(description["description"])
        object_name = f"description_{description['id']}_input"
        description_input.setObjectName(object_name)
        description_input.setFixedSize(550, 30)

        form_layout_right.addRow(description_label, description_input)
        input_names.append(object_name)

    conn.close()

    return form_layout_right
