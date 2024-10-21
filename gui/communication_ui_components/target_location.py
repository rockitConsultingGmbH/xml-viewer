from PyQt5.QtWidgets import QFormLayout, QLineEdit, QLabel, QCheckBox, QHBoxLayout, QSpacerItem, QSizePolicy

from common.connection_manager import ConnectionManager
from database.utils import select_from_location


def create_target_location_form(label_children_style, communication_id):
    target_locations_form_layout = QFormLayout()

    conn_manager = ConnectionManager().get_instance()
    conn = conn_manager.get_db_connection()
    cursor = conn.cursor()
    targetLocations = select_from_location(cursor, communication_id, 'targetLocation').fetchall()

    for targetLocation in targetLocations:
        target_label = QLabel("Target")
        target_label.setFixedWidth(70)
        target_label.setStyleSheet(label_children_style)
        target_input = QLineEdit()
        target_input.setFixedHeight(30)
        target_input.setObjectName(f"target_{targetLocation['id']}_input")

        target_locations_form_layout.addRow(target_label, target_input)
        target_locations_form_layout.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))

        hbox_columns = QHBoxLayout()

        left_column_layout = QFormLayout()
        left_column_layout.setVerticalSpacing(15)

        userid_label = QLabel("User ID")
        userid_label.setStyleSheet(label_children_style)
        userid_input = QLineEdit()
        userid_input.setObjectName(f"userid_target_{targetLocation['id']}_input")
        userid_input.setFixedHeight(30)

        location_id_label = QLabel("Location ID")
        location_id_label.setStyleSheet(label_children_style)
        location_id_label.setFixedWidth(100)
        location_id_input = QLineEdit()
        location_id_input.setObjectName(f"location_id_target_{targetLocation['id']}_input")
        location_id_input.setFixedHeight(30)

        use_local_filename_checkbox = QCheckBox("Use Local Filename")
        use_local_filename_checkbox.setStyleSheet(label_children_style)
        use_local_filename_checkbox.setObjectName(f"use_local_filename_checkbox_target_{targetLocation['id']}")

        use_path_from_config_checkbox = QCheckBox("Use Path From Config")
        use_path_from_config_checkbox.setStyleSheet(label_children_style)
        use_path_from_config_checkbox.setObjectName(f"use_path_from_config_checkbox_target_{targetLocation['id']}")

        left_column_layout.addRow(userid_label, userid_input)
        left_column_layout.addRow(location_id_label, location_id_input)
        left_column_layout.addRow(use_local_filename_checkbox)
        left_column_layout.addRow(use_path_from_config_checkbox)

        left_column_with_margin = QHBoxLayout()
        left_margin = QSpacerItem(90, 0, QSizePolicy.Fixed, QSizePolicy.Minimum)
        left_column_with_margin.addItem(left_margin)
        left_column_with_margin.addLayout(left_column_layout)

        right_column_layout = QFormLayout()
        right_column_layout.setVerticalSpacing(15)

        password_label = QLabel("Password")
        password_label.setStyleSheet(label_children_style)
        password_label.setFixedWidth(80)
        password_input = QLineEdit()
        password_input.setObjectName(f"password_target_{targetLocation['id']}_input")
        password_input.setFixedHeight(30)

        description_target_label = QLabel("Description")
        description_target_label.setStyleSheet(label_children_style)
        description_target_label.setFixedWidth(100)
        description_target_input = QLineEdit()
        description_target_input.setObjectName(f"description_target_{targetLocation['id']}_input")
        description_target_input.setFixedHeight(30)

        target_history_days_checkbox = QCheckBox("Target History Days")
        target_history_days_checkbox.setStyleSheet(label_children_style)
        target_history_days_checkbox.setObjectName(f"target_history_days_checkbox_{targetLocation['id']}")

        rename_existing_file_checkbox = QCheckBox("Rename Existing File")
        rename_existing_file_checkbox.setStyleSheet(label_children_style)
        rename_existing_file_checkbox.setObjectName(f"rename_existing_file_checkbox_{targetLocation['id']}")

        target_must_be_archived_checkbox = QCheckBox("Target Must Be Archived")
        target_must_be_archived_checkbox.setStyleSheet(label_children_style)
        target_must_be_archived_checkbox.setObjectName(f"target_must_be_archived_checkbox_{targetLocation['id']}")

        right_column_layout.addRow(password_label, password_input)
        right_column_layout.addRow(description_target_label, description_target_input)
        right_column_layout.addRow(target_history_days_checkbox)
        right_column_layout.addRow(rename_existing_file_checkbox)
        right_column_layout.addRow(target_must_be_archived_checkbox)

        hbox_columns.addLayout(left_column_with_margin)
        hbox_columns.addSpacing(50)
        hbox_columns.addLayout(right_column_layout)

        target_locations_form_layout.addRow(hbox_columns)
        target_locations_form_layout.addItem(
            QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))

    conn.close()
    return target_locations_form_layout
