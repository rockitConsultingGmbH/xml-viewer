from PyQt5.QtWidgets import QFormLayout, QLineEdit, QLabel, QCheckBox, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtWidgets import QFormLayout, QLineEdit, QLabel
from controllers.utils.get_db_connection import get_db_connection
from database.utils import select_from_location

def create_target_location_form(label_children_style, communication_id):
    target_locations_form_layout = QFormLayout()

    conn, cursor = get_db_connection()
    targetLocations = select_from_location(cursor, communication_id, 'targetLocation').fetchall()

    for tl in targetLocations:
        target_location_form_layout = QFormLayout()

        target_label= QLabel("Target")
        target_label.setFixedWidth(70)
        target_label.setStyleSheet(label_children_style)

        target_input = QLineEdit()
        target_input.setFixedHeight(30)
        target_input.setObjectName(f"target_{tl['id']}_input")

        spacer_item = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        left_column_layout = QFormLayout()
        left_column_layout.setVerticalSpacing(15)
        left_column_layout.addItem(spacer_item)

        userid_target_label = QLabel("User ID")
        userid_target_label.setStyleSheet(label_children_style)
        userid_target_label.setFixedWidth(100)
        userid_target_input = QLineEdit()
        userid_target_input.setObjectName(f"userid_{tl['id']}_input")
        userid_target_input.setFixedHeight(30)

        location_id_target_label = QLabel("Location ID")
        location_id_target_label.setStyleSheet(label_children_style)
        location_id_target_input = QLineEdit()
        location_id_target_input.setObjectName(f"location_id_{tl['id']}_input")
        location_id_target_input.setFixedHeight(30)

        use_local_filename_checkbox_target = QCheckBox("Use Local Filename")
        use_local_filename_checkbox_target.setStyleSheet(label_children_style)
        use_local_filename_checkbox_target.setObjectName(f"use_local_filename_checkbox_target_{tl['id']}")

        use_path_from_config_checkbox_target = QCheckBox("Use Path From Config")
        use_path_from_config_checkbox_target.setStyleSheet(label_children_style)
        use_path_from_config_checkbox_target.setObjectName(f"use_path_from_config_checkbox_target_{tl['id']}")

        left_column_layout.addRow(userid_target_label, userid_target_input)
        left_column_layout.addRow(location_id_target_label, location_id_target_input)
        left_column_layout.addRow(use_local_filename_checkbox_target)
        left_column_layout.addRow(use_path_from_config_checkbox_target)

        right_column_layout = QFormLayout()
        right_column_layout.setVerticalSpacing(15)
        right_column_layout.addItem(spacer_item)

        password_target_label = QLabel("Password")
        password_target_label.setStyleSheet(label_children_style)
        password_target_label.setFixedWidth(80)
        password_target_input = QLineEdit()
        password_target_input.setObjectName(f"password_target_{tl['id']}_input")
        password_target_input.setFixedHeight(30)

        description_target_label = QLabel("Description")
        description_target_label.setStyleSheet(label_children_style)
        description_target_input = QLineEdit()
        description_target_input.setObjectName(f"description_target_{tl['id']}_input")
        description_target_input.setFixedHeight(30)

        target_history_days_checkbox = QCheckBox("Target History Days")
        target_history_days_checkbox.setStyleSheet(label_children_style)
        target_history_days_checkbox.setObjectName(f"target_history_days_checkbox_{tl['id']}")

        rename_existing_file_checkbox = QCheckBox("Rename Existing File")
        rename_existing_file_checkbox.setStyleSheet(label_children_style)
        rename_existing_file_checkbox.setObjectName(f"rename_existing_file_checkbox_{tl['id']}")

        target_must_be_archived_checkbox = QCheckBox("Target Must Be Archived")
        target_must_be_archived_checkbox.setStyleSheet(label_children_style)
        target_must_be_archived_checkbox.setObjectName(f"target_must_be_archived_checkbox_{tl['id']}")

        right_column_layout.addRow(password_target_label, password_target_input)
        right_column_layout.addRow(description_target_label, description_target_input)
        right_column_layout.addRow(target_history_days_checkbox)
        right_column_layout.addRow(rename_existing_file_checkbox)
        right_column_layout.addRow(target_must_be_archived_checkbox)

        hbox_columns = QHBoxLayout()
        left_margin = QSpacerItem(90, 0, QSizePolicy.Fixed, QSizePolicy.Minimum)
        hbox_columns.addItem(left_margin)
        hbox_columns.addLayout(left_column_layout)
        hbox_columns.addSpacing(50)
        hbox_columns.addLayout(right_column_layout)

        target_location_form_layout.addRow(target_label, target_input)
        target_location_form_layout.addRow(hbox_columns)
        target_locations_form_layout.addRow(target_location_form_layout)

    conn.close()
    return target_locations_form_layout