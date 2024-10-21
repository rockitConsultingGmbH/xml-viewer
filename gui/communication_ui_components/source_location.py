from PyQt5.QtWidgets import QLabel, QCheckBox, QLineEdit, QPushButton, QFormLayout, QHBoxLayout, \
    QSpacerItem, QSizePolicy
from utils.clickable_label import ClickableLabel
from gui.communication_ui_components.target_location import create_target_location_form


def create_locations_group(group_layout, communication_id):
    label_style = "border: none; font-size: 14px; font-weight: bold;"
    label_children_style = "border: none; font-size: 14px;"
    form_layout = QFormLayout()
    form_layout.setHorizontalSpacing(20)
    form_layout.setVerticalSpacing(15)

    spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
    group_layout.addItem(spacer)

    source_location_label = QLabel("Source Location")
    source_location_label.setStyleSheet(label_style)
    group_layout.addWidget(source_location_label)

    source_label = ClickableLabel("Source")
    source_label.setStyleSheet(label_children_style)
    source_label.setFixedWidth(70)
    source_input = QLineEdit()
    source_input.setObjectName("source_input")
    source_input.setFixedHeight(30)

    form_layout.addRow(source_label, source_input)

    hbox_columns = QHBoxLayout()

    left_column_layout = QFormLayout()
    left_column_layout.setVerticalSpacing(15)

    userid_label = QLabel("User ID")
    userid_label.setStyleSheet(label_children_style)
    userid_input = QLineEdit()
    userid_input.setObjectName("userid_source_input")
    userid_input.setFixedHeight(30)

    location_id_label = QLabel("Location ID")
    location_id_label.setStyleSheet(label_children_style)
    location_id_label.setFixedWidth(100)
    location_id_input = QLineEdit()
    location_id_input.setObjectName("location_id_input")
    location_id_input.setFixedHeight(30)

    use_local_filename_checkbox = QCheckBox("Use Local Filename")
    use_local_filename_checkbox.setStyleSheet(label_children_style)
    use_local_filename_checkbox.setObjectName("use_local_filename_checkbox")

    use_path_from_config_checkbox = QCheckBox("Use Path From Config")
    use_path_from_config_checkbox.setStyleSheet(label_children_style)
    use_path_from_config_checkbox.setObjectName("use_path_from_config_checkbox")

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
    password_input.setObjectName("password_source_input")
    password_input.setFixedHeight(30)

    description_source_label = QLabel("Description")
    description_source_label.setStyleSheet(label_children_style)
    description_source_label.setFixedWidth(100)
    description_source_input = QLineEdit()
    description_source_input.setObjectName("description_source_input")
    description_source_input.setFixedHeight(30)

    target_history_days_checkbox = QCheckBox("Target History Days")
    target_history_days_checkbox.setStyleSheet(label_children_style)
    target_history_days_checkbox.setObjectName("target_history_days_checkbox")

    rename_existing_file_checkbox = QCheckBox("Rename Existing File")
    rename_existing_file_checkbox.setStyleSheet(label_children_style)
    rename_existing_file_checkbox.setObjectName("rename_existing_file_checkbox")

    target_must_be_archived_checkbox = QCheckBox("Target Must Be Archived")
    target_must_be_archived_checkbox.setStyleSheet(label_children_style)
    target_must_be_archived_checkbox.setObjectName("target_must_be_archived_checkbox")

    right_column_layout.addRow(password_label, password_input)
    right_column_layout.addRow(description_source_label, description_source_input)
    right_column_layout.addRow(target_history_days_checkbox)
    right_column_layout.addRow(rename_existing_file_checkbox)
    right_column_layout.addRow(target_must_be_archived_checkbox)

    hbox_columns.addLayout(left_column_with_margin)
    hbox_columns.addSpacing(50)
    hbox_columns.addLayout(right_column_layout)

    form_layout.addRow(hbox_columns)

    form_layout.addItem(QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

    target_label = QLabel("Target Location(s)")
    target_label.setFixedWidth(145)
    target_label.setStyleSheet(label_style)

    add_button = QPushButton("+")
    add_button.setFixedSize(30, 30)
    add_button.setObjectName("addButton")
    add_button.setStyleSheet("""
        #addButton {
            background-color: #f0f0f0;
            border: 1px solid #A9A9A9;
            border-radius: 15px;
            text-align: center;
            font-size: 16px;
            font-weight: bold;
        }
        #addButton:hover {
            background-color: #dcdcdc;
            cursor: pointer;
        }
        #addButton:pressed {
            background-color: #c0c0c0;
        }
    """)

    hbox_target = QHBoxLayout()
    hbox_target.addWidget(target_label)
    hbox_target.addWidget(add_button)

    form_layout.addRow(hbox_target)

    target_locations_form_layout = create_target_location_form(label_children_style, communication_id)
    form_layout.addRow(target_locations_form_layout)

    group_layout.addLayout(form_layout)
