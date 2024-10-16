from PyQt5.QtWidgets import QFormLayout, QLineEdit, QLabel, QCheckBox, QHBoxLayout, QSpacerItem, QSizePolicy

def create_target_location_form(form_layout, label_children_style):
    target_label_2 = QLabel("Target")
    target_label_2.setFixedWidth(70)
    target_label_2.setStyleSheet(label_children_style)

    target_input_2 = QLineEdit()
    target_input_2.setFixedHeight(30)
    target_input_2.setObjectName("target_second_input")

    left_column_layout_2 = QFormLayout()
    left_column_layout_2.setVerticalSpacing(15)

    userid_target_label_2 = QLabel("User ID")
    userid_target_label_2.setStyleSheet(label_children_style)
    userid_target_label_2.setFixedWidth(100)
    userid_target_input_2 = QLineEdit()
    userid_target_input_2.setObjectName("userid_target_second_input")
    userid_target_input_2.setFixedHeight(30)

    location_id_target_label_2 = QLabel("Location ID")
    location_id_target_label_2.setStyleSheet(label_children_style)
    location_id_target_input_2 = QLineEdit()
    location_id_target_input_2.setObjectName("location_id_target_second_input")
    location_id_target_input_2.setFixedHeight(30)

    use_local_filename_checkbox_target_2 = QCheckBox("Use Local Filename")
    use_local_filename_checkbox_target_2.setStyleSheet(label_children_style)
    use_local_filename_checkbox_target_2.setObjectName("use_local_filename_checkbox_target_second")

    use_path_from_config_checkbox_target_2 = QCheckBox("Use Path From Config")
    use_path_from_config_checkbox_target_2.setStyleSheet(label_children_style)
    use_path_from_config_checkbox_target_2.setObjectName("use_path_from_config_checkbox_target_second")

    left_column_layout_2.addRow(userid_target_label_2, userid_target_input_2)
    left_column_layout_2.addRow(location_id_target_label_2, location_id_target_input_2)
    left_column_layout_2.addRow(use_local_filename_checkbox_target_2)
    left_column_layout_2.addRow(use_path_from_config_checkbox_target_2)

    right_column_layout_2 = QFormLayout()
    right_column_layout_2.setVerticalSpacing(15)

    password_target_label_2 = QLabel("Password")
    password_target_label_2.setStyleSheet(label_children_style)
    password_target_label_2.setFixedWidth(80)
    password_target_input_2 = QLineEdit()
    password_target_input_2.setObjectName("password_target_second_input")
    password_target_input_2.setFixedHeight(30)

    description_target_label_2 = QLabel("Description")
    description_target_label_2.setStyleSheet(label_children_style)
    description_target_input_2 = QLineEdit()
    description_target_input_2.setObjectName("description_target_second_input")
    description_target_input_2.setFixedHeight(30)

    target_history_days_checkbox_2 = QCheckBox("Target History Days")
    target_history_days_checkbox_2.setStyleSheet(label_children_style)
    target_history_days_checkbox_2.setObjectName("target_history_days_checkbox_second")

    rename_existing_file_checkbox_2 = QCheckBox("Rename Existing File")
    rename_existing_file_checkbox_2.setStyleSheet(label_children_style)
    rename_existing_file_checkbox_2.setObjectName("rename_existing_file_checkbox_second")

    target_must_be_archived_checkbox_2 = QCheckBox("Target Must Be Archived")
    target_must_be_archived_checkbox_2.setStyleSheet(label_children_style)
    target_must_be_archived_checkbox_2.setObjectName("target_must_be_archived_checkbox_second")

    right_column_layout_2.addRow(password_target_label_2, password_target_input_2)
    right_column_layout_2.addRow(description_target_label_2, description_target_input_2)
    right_column_layout_2.addRow(target_history_days_checkbox_2)
    right_column_layout_2.addRow(rename_existing_file_checkbox_2)
    right_column_layout_2.addRow(target_must_be_archived_checkbox_2)

    hbox_columns_2 = QHBoxLayout()
    left_margin_2 = QSpacerItem(90, 0, QSizePolicy.Fixed, QSizePolicy.Minimum)
    hbox_columns_2.addItem(left_margin_2)
    hbox_columns_2.addLayout(left_column_layout_2)
    hbox_columns_2.addSpacing(50)
    hbox_columns_2.addLayout(right_column_layout_2)

    form_layout.addRow(target_label_2, target_input_2)
    form_layout.addRow(hbox_columns_2)