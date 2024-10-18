from PyQt5.QtWidgets import QFormLayout, QLineEdit, QLabel, QCheckBox, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtWidgets import QFormLayout, QLineEdit, QLabel
from controllers.utils.get_db_connection import get_db_connection
from database.utils import select_from_location

def create_target_location_form(label_children_style, communication_id):
    target_locations_form_layout = QFormLayout()

    conn, cursor = get_db_connection()
    targetLocations = select_from_location(cursor, communication_id, 'targetLocation').fetchall()

    for targetLocation in targetLocations:
        target_loc_form_layout = QFormLayout()

        target_label= QLabel("Target")
        target_label.setFixedWidth(70)
        target_label.setStyleSheet(label_children_style)
        target_input = QLineEdit()
        target_input.setFixedHeight(30)
        target_input.setObjectName(f"target_{targetLocation['id']}_input")

        userid_target_label = QLabel("User ID")
        userid_target_label.setStyleSheet(label_children_style)
        userid_target_label.setFixedWidth(100)
        userid_target_input = QLineEdit()
        userid_target_input.setObjectName(f"userid_target_{targetLocation['id']}_input")
        userid_target_input.setFixedHeight(30)

        target_loc_form_layout.addRow(target_label, target_input)
        target_loc_form_layout.addRow(userid_target_label, userid_target_input)
        target_locations_form_layout.addRow(target_loc_form_layout)

    conn.close()
    return target_locations_form_layout