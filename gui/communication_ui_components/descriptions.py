from PyQt5.QtWidgets import QFormLayout, QLineEdit, QLabel, QHBoxLayout, QPushButton
from common.connection_manager import ConnectionManager
from database.utils import select_from_description
from gui.common_components.delete_elements import delete_field

input_names = []

def create_description_form(communication_id):
    form_layout_right = QFormLayout()

    conn_manager = ConnectionManager().get_instance()
    conn = conn_manager.get_db_connection()
    cursor = conn.cursor()
    descriptions = select_from_description(cursor, communication_id)

    for description in descriptions:
        add_description_fields(form_layout_right, description)

    conn.close()
    return form_layout_right

def add_description_fields(form_layout_right, description):
    description_label = QLabel("Description")
    description_label.setFixedWidth(80)

    description_input = QLineEdit(description["description"])
    object_name = f"description_{description['id']}_input"
    description_input.setObjectName(object_name)
    description_input.setFixedSize(550, 30)

    delete_descriptions_button = QPushButton("-")
    delete_descriptions_button.setObjectName("deleteButton")
    delete_descriptions_button.setFixedSize(30, 30)

    hbox_layout = QHBoxLayout()
    hbox_layout.addWidget(description_input)
    hbox_layout.addWidget(delete_descriptions_button)

    form_layout_right.addRow(description_label, hbox_layout)

    input_names.append(object_name)

    delete_descriptions_button.clicked.connect(lambda: delete_field(form_layout_right, description_label, hbox_layout))
