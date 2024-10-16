from PyQt5.QtWidgets import QFormLayout, QLineEdit, QLabel
from controllers.utils.get_db_connection import get_db_connection
from database.utils import select_from_description
from utils.clickable_label import ClickableLabel

def create_description_form(label_style, communication_id):

    form_layout_right = QFormLayout()
    description_label = ClickableLabel("Description(s)")
    description_label.setStyleSheet(label_style)

    conn, cursor = get_db_connection()
    descriptions = select_from_description(cursor, communication_id)

    for description in descriptions:
        description_label = QLabel(description["descriptionType"])
        description_input = QLineEdit(description["description"])
        description_input.setObjectName(f"description_[{description['id']}]_input")
        description_input.setFixedSize(550, 30)

        form_layout_right.addRow(description_label, description_input)

    conn.close()

    return form_layout_right
