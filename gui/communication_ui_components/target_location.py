from PyQt5.QtWidgets import QFormLayout, QLineEdit, QLabel, QCheckBox, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QWidget, QPushButton

from common.connection_manager import ConnectionManager
from database.utils import select_from_location

from gui.common_components.clickable_label import ClickableLabel
from gui.common_components.toggle_inputs import toggle_inputs
from gui.common_components.delete_elements import delete_all_fields
																   


def create_target_location_form(communication_id):
    target_locations_form_layout = QFormLayout()

    conn_manager = ConnectionManager().get_instance()
    conn = conn_manager.get_db_connection()
    cursor = conn.cursor()
    targetLocations = select_from_location(cursor, communication_id, 'targetLocation').fetchall()

    for targetLocation in targetLocations:
        add_target_location_fields(target_locations_form_layout, targetLocation, toggle_inputs)

    conn.close()
    return target_locations_form_layout


def add_target_location_fields(layout, targetLocation, toggle_inputs):
    target_labels, target_inputs, target_checkboxes = [], [], []

    # Create a QWidget to contain the target box layout
    target_box_widget = QWidget()
    target_box_widget.setObjectName(f"target_box_{targetLocation['id']}")
    target_box_widget.setProperty("target_id", targetLocation['id'])

    # Main layout within the target_box_widget
    target_box = QVBoxLayout(target_box_widget)

    # Target label and input
    # Target label, input, and delete button
    target_label = ClickableLabel("Target")
    target_label.setFixedWidth(90)
    target_input = QLineEdit()
    target_input.setFixedHeight(30)
    target_input.setObjectName(f"target_{targetLocation['id']}_input")
    
    target_delete_button = QPushButton("-")
    target_delete_button.setObjectName("deleteButton")
    target_delete_button.setFixedSize(30, 30)
    
    # Create a horizontal layout to hold the label, input, and button
    target_row_layout = QHBoxLayout()
    target_row_layout.addWidget(target_label)
    target_row_layout.addWidget(target_input)
    target_row_layout.addWidget(target_delete_button)
    
    # Add the horizontal layout to the form layout
    upper_layout = QFormLayout()
    upper_layout.addRow(target_row_layout)
    upper_layout.addItem(QSpacerItem(0, 15, QSizePolicy.Minimum, QSizePolicy.Fixed))
	
    # Add the form layout to target_box
    target_box.addLayout(upper_layout)

    hbox_columns = QHBoxLayout()

    left_column_layout = QFormLayout()
    left_column_layout.setVerticalSpacing(15)

    userid_label = QLabel("User ID")
    userid_input = QLineEdit()
    userid_input.setObjectName(f"userid_target_{targetLocation['id']}_input")
    userid_input.setFixedHeight(30)

    location_id_label = QLabel("Location ID")
    location_id_label.setFixedWidth(100)
    location_id_input = QLineEdit()
    location_id_input.setObjectName(f"location_id_target_{targetLocation['id']}_input")
    location_id_input.setFixedHeight(30)

    use_local_filename_checkbox = QCheckBox("Use Local Filename")
    use_local_filename_checkbox.setObjectName(f"use_local_filename_checkbox_target_{targetLocation['id']}")

    use_path_from_config_checkbox = QCheckBox("Use Path From Config")
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
    password_label.setFixedWidth(80)
    password_input = QLineEdit()
    password_input.setObjectName(f"password_target_{targetLocation['id']}_input")
    password_input.setFixedHeight(30)

    target_description_label = QLabel("Description")
    target_description_label.setFixedWidth(100)
    target_description_input = QLineEdit()
    target_description_input.setObjectName(f"target_description_{targetLocation['id']}_input")
    target_description_input.setFixedHeight(30)

    target_history_days_checkbox = QCheckBox("Target History Days")
    target_history_days_checkbox.setObjectName(f"target_history_days_checkbox_{targetLocation['id']}")

    rename_existing_file_checkbox = QCheckBox("Rename Existing File")
    rename_existing_file_checkbox.setObjectName(f"rename_existing_file_checkbox_{targetLocation['id']}")

    target_must_be_archived_checkbox = QCheckBox("Target Must Be Archived")
    target_must_be_archived_checkbox.setObjectName(f"target_must_be_archived_checkbox_{targetLocation['id']}")

    right_column_layout.addRow(password_label, password_input)
    right_column_layout.addRow(target_description_label, target_description_input)
    right_column_layout.addRow(target_history_days_checkbox)
    right_column_layout.addRow(rename_existing_file_checkbox)
    right_column_layout.addRow(target_must_be_archived_checkbox)

    hbox_columns.addLayout(left_column_with_margin)
    hbox_columns.addSpacing(50)
    hbox_columns.addLayout(right_column_layout)

    target_box.addLayout(hbox_columns)

    layout.addRow(target_box_widget)
    layout.addItem(QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

    target_labels.extend([userid_label, location_id_label, password_label, target_description_label])
    target_inputs.extend([userid_input, location_id_input, password_input, target_description_input])
    target_checkboxes.extend([use_local_filename_checkbox, use_path_from_config_checkbox, target_history_days_checkbox,
                              rename_existing_file_checkbox, target_must_be_archived_checkbox])

    target_label.mousePressEvent = lambda event: toggle_inputs(target_labels, target_inputs, target_checkboxes)
    #target_delete_button.clicked.connect(lambda: delete_all_fields([target_box, left_column_layout, right_column_layout, layout]))
																																												 