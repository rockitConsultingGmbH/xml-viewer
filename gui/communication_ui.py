from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QGroupBox, QHBoxLayout, QCheckBox, QPushButton, QLabel, \
    QLineEdit, QFormLayout, QSpacerItem, QSizePolicy, QScrollArea, QWidget, QFrame, QComboBox

from database.populating.communication_table_data import save_communication_data

# Clickable Label class for transforming labels into clickable buttons
class ClickableLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)


# Group Builder
from PyQt5.QtWidgets import QMessageBox


def setup_right_interface(right_widget, communication_id):
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setStyleSheet("QScrollArea { border: none; } QWidget { border: none; } "
                              "QLineEdit, QComboBox, QPushButton { border: 1px solid gray; }")

    scroll_content = QWidget()
    scroll_layout = QVBoxLayout(scroll_content)

    button_layout = QHBoxLayout()
    button_layout.addStretch()

    reset_button = QPushButton("Reset")
    reset_button.setFixedSize(100, 30)
    reset_button.setObjectName("resetButton")
    reset_button.setStyleSheet("""
        #resetButton {
            background-color: #9c9c9c; color: white;
        }

        #resetButton:hover {
            background-color: #8c8c8c;
        }

        #resetButton:pressed {
            background-color: #2d2d33;
        }
    """)

    save_button = QPushButton("Save")
    save_button.setFixedSize(100, 30)
    save_button.setObjectName("saveButton")
    save_button.setStyleSheet("""
        #saveButton {
            background-color: #db0d0d; color: white;
        }

        #saveButton:hover {
            background-color: #b00c0c;
        }

        #saveButton:pressed {
            background-color: #910909;
        }
    """)

    def save_and_show_message():
        save_communication_data(communication_id)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Changes in Communication have been successfully saved.")
        msg.setWindowTitle("Save Successful")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    save_button.clicked.connect(save_and_show_message)

    button_layout.addWidget(reset_button)
    button_layout.addWidget(save_button)

    scroll_layout.addLayout(button_layout)

    create_group("Overview", scroll_layout)
    create_group("Locations", scroll_layout)
    create_group("Settings", scroll_layout)
    create_group("Pattern", scroll_layout)
    create_group("PostCommand(s)", scroll_layout)

    scroll_area.setWidget(scroll_content)

    right_layout = QVBoxLayout(right_widget)
    right_layout.addWidget(scroll_area)
    right_widget.setLayout(right_layout)


# Group interface builder
def create_group(group_name, layout):
    global input_labels, input_fields, source_labels, source_inputs, target_labels, target_inputs, settings_labels, \
        settings_inputs, other_settings_labels, other_settings_inputs, post_command_labels, post_command_inputs
    group_box = QGroupBox(group_name)
    group_box.setStyleSheet("QGroupBox { font-weight: bold; font-size: 15px; border: none; }")
    group_layout = QVBoxLayout()

    if group_name == "Overview":
        input_labels = []
        input_fields = []
    elif group_name == "Locations":
        source_labels = []
        source_inputs = []
        target_labels = []
        target_inputs = []
    elif group_name == "Settings":
        settings_labels = []
        settings_inputs = []
        other_settings_labels = []
        other_settings_inputs = []

    # Overview group
    if group_name == "Overview":
        label_style = "border: none; font-size: 14px;"
        checkbox_style = "border: none;"

        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        group_layout.addItem(spacer)

        hbox1 = QHBoxLayout()
        checkbox = QCheckBox("Polling aktiviert")
        checkbox.setObjectName("polling_activate_checkbox")
        checkbox.setStyleSheet(checkbox_style)
        hbox1.addWidget(checkbox)
        hbox1.addStretch()
        group_layout.addLayout(hbox1)

        hbox_columns = QHBoxLayout()

        form_layout_left = QFormLayout()

        name_label = QLabel("Name")
        name_label.setStyleSheet(label_style)
        name_input = QLineEdit()
        name_input.setFixedSize(450, 30)
        name_input.setObjectName("name_input")
        form_layout_left.addRow(name_label, name_input)

        alt_name_label = QLabel("Alternate Namelist")
        alt_name_label.setStyleSheet(label_style)
        alt_name_input = QLineEdit()
        alt_name_input.setObjectName("alt_name_input")
        alt_name_input.setFixedSize(400, 30)

        go_button = QPushButton("GO")
        go_button.setObjectName("goButton")
        go_button.setFixedSize(43, 30)
        go_button.setStyleSheet("""
            #goButton {
                background-color: #f0f0f0;
                border: 1px solid #A9A9A9;
            }
            #goButton:hover {
                background-color: #dcdcdc;
                cursor: pointer;
            }
            #goButton:pressed {
                background-color: #c0c0c0;
            }
        """)

        hbox_alt_name = QHBoxLayout()
        hbox_alt_name.addWidget(alt_name_input)
        hbox_alt_name.addWidget(go_button)
        form_layout_left.addRow(alt_name_label, hbox_alt_name)

        hbox_columns.addLayout(form_layout_left)
        hbox_columns.addStretch(1)

        form_layout_right = QFormLayout()

        description_label = ClickableLabel("Description(s)")
        description_label.setStyleSheet(label_style)

        description_input = QLineEdit()
        description_input.setObjectName("description_input")
        description_input.setFixedSize(550, 30)

        form_layout_right.addRow(description_label, description_input)

        description_1_label = QLabel("Description")
        description_1_label.setStyleSheet(label_style)
        description_1_input = QLineEdit()
        description_1_input.setFixedSize(550, 30)
        description_1_input.setObjectName("description_1_input")

        description_2_label = QLabel("Description")
        description_2_label.setStyleSheet(label_style)
        description_2_input = QLineEdit()
        description_2_input.setFixedSize(550, 30)
        description_2_input.setObjectName("description_2_input")

        description_3_label = QLabel("Description")
        description_3_label.setStyleSheet(label_style)
        description_3_input = QLineEdit()
        description_3_input.setFixedSize(550, 30)
        description_3_input.setObjectName("description_3_input")

        form_layout_right.addRow(description_1_label, description_1_input)
        form_layout_right.addRow(description_2_label, description_2_input)
        form_layout_right.addRow(description_3_label, description_3_input)

        input_labels = [description_1_label, description_2_label, description_3_label]
        input_fields = [description_1_input, description_2_input, description_3_input]

        description_label.mousePressEvent = lambda event: toggle_inputs(input_labels, input_fields)

        hbox_columns.addLayout(form_layout_right)
        group_layout.addLayout(hbox_columns)

    # Locations group
    elif group_name == "Locations":
        label_style = "border: none; font-size: 14px; font-weight: bold;"
        label_children_style = "border: none; font-size: 14px;"
        form_layout = QFormLayout()
        form_layout.setHorizontalSpacing(10)
        form_layout.setVerticalSpacing(15)

        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        group_layout.addItem(spacer)

        source_label = ClickableLabel("Source")
        source_label.setStyleSheet(label_children_style)
        source_input = QLineEdit()
        source_input.setObjectName("source_input")
        source_input.setFixedHeight(30)

        form_layout.addRow(source_label, source_input)

        hbox_userid_password = QHBoxLayout()

        hbox_userid_password.addSpacing(55)

        userid_label = QLabel("UserID")
        userid_label.setStyleSheet(label_children_style)
        userid_label.setFixedWidth(60)
        userid_input = QLineEdit()
        userid_input.setObjectName("userid_source_input")
        userid_input.setFixedSize(450, 30)

        password_label = QLabel("Password")
        password_label.setStyleSheet(label_children_style)
        password_label.setFixedWidth(80)
        password_input = QLineEdit()
        password_input.setObjectName("password_source_input")
        password_input.setFixedSize(450, 30)

        hbox_userid_password.addWidget(userid_label)
        hbox_userid_password.addWidget(userid_input)
        hbox_userid_password.addStretch()
        hbox_userid_password.addWidget(password_label)
        hbox_userid_password.addWidget(password_input)

        form_layout.addRow(hbox_userid_password)

        source_labels.append(userid_label)
        source_labels.append(password_label)
        source_inputs.append(userid_input)
        source_inputs.append(password_input)

        source_label.mousePressEvent = lambda event: toggle_inputs(source_labels, source_inputs)

        form_layout.addItem(QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        target_label = QLabel("Target Locations(s)")
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

        target_count = 5
        for i in range(1, target_count + 1):
            target_label = ClickableLabel(f"Target ({i})")
            target_label.setFixedWidth(130)
            target_label.setStyleSheet(label_children_style)

            target_input = QLineEdit()
            target_input.setFixedHeight(30)
            target_input.setObjectName(f"target_{i}_input")

            userid_target_label = QLabel("UserID")
            userid_target_label.setStyleSheet(label_children_style)
            userid_target_label.setFixedWidth(60)
            userid_target_input = QLineEdit()
            userid_target_input.setFixedSize(450, 30)
            userid_target_input.setObjectName(f"userid_target_{i}_input")

            password_target_label = QLabel("Password")
            password_target_label.setStyleSheet(label_children_style)
            password_target_label.setFixedWidth(80)
            password_target_input = QLineEdit()
            password_target_input.setFixedSize(450, 30)
            password_target_input.setObjectName(f"password_target_{i}_input")

            target_labels.append(userid_target_label)
            target_labels.append(password_target_label)
            target_inputs.append(userid_target_input)
            target_inputs.append(password_target_input)

            hbox_target_row = QHBoxLayout()
            hbox_target_row.addWidget(target_label)
            hbox_target_row.addWidget(target_input)

            hbox_userid_target_password_row = QHBoxLayout()
            hbox_userid_target_password_row.addItem(
                QSpacerItem(130, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))  # Add spacer
            hbox_userid_target_password_row.addWidget(userid_target_label)
            hbox_userid_target_password_row.addWidget(userid_target_input)
            hbox_userid_target_password_row.addStretch()
            hbox_userid_target_password_row.addWidget(password_target_label)
            hbox_userid_target_password_row.addWidget(password_target_input)

            form_layout.addRow(hbox_target_row)
            form_layout.addRow(hbox_userid_target_password_row)

            target_label.mousePressEvent = lambda event, labels=[userid_target_label, password_target_label], \
                                                  inputs=[userid_target_input, password_target_input]: (
                toggle_inputs(labels, inputs))

        group_layout.addLayout(form_layout)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("QFrame { background-color: black; color: black; }")
        layout.addWidget(line)

    # Settings group
    elif group_name == "Settings":
        label_style = "border: none; font-size: 14px; font-weight: bold;"
        label_children_style = "border: none; font-size: 14px;"
        checkbox_style = "border: none;"

        hbox = QHBoxLayout()

        group_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        polling_label = ClickableLabel("Polling")
        polling_label.setFixedWidth(120)
        polling_label.setStyleSheet(label_style)
        hbox.addWidget(polling_label)

        polling_active_checkbox = QCheckBox("Polling active")
        polling_active_checkbox.setStyleSheet(checkbox_style)
        polling_active_checkbox.setFixedWidth(200)

        poll_until_found_checkbox = QCheckBox("Poll until found")
        poll_until_found_checkbox.setObjectName("poll_until_found_checkbox")
        poll_until_found_checkbox.setStyleSheet(checkbox_style)
        poll_until_found_checkbox.setFixedWidth(200)

        no_transfer_checkbox = QCheckBox("No transfer")
        no_transfer_checkbox.setObjectName("no_transfer_checkbox")
        no_transfer_checkbox.setStyleSheet(checkbox_style)

        hbox.addWidget(polling_active_checkbox)
        hbox.addWidget(poll_until_found_checkbox)
        hbox.addWidget(no_transfer_checkbox)

        group_layout.addLayout(hbox)

        group_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        form_layout_left = QVBoxLayout()

        hbox_input1 = QHBoxLayout()
        hbox_input1.addItem(QSpacerItem(125, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))
        input1_label = QLabel("Beförderung ab")
        input1_label.setFixedWidth(100)
        input1_label.setStyleSheet(label_children_style)
        input1 = QLineEdit()
        input1.setObjectName("befoerderung_ab_input")
        input1.setFixedSize(450, 30)
        hbox_input1.addWidget(input1_label)
        hbox_input1.addWidget(input1)
        form_layout_left.addLayout(hbox_input1)

        settings_labels.append(input1_label)
        settings_inputs.append(input1)

        hbox_input2 = QHBoxLayout()
        hbox_input2.addItem(QSpacerItem(125, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))
        input2_label = QLabel("Poll Intervall")
        input2_label.setFixedWidth(100)
        input2_label.setStyleSheet(label_children_style)
        input2 = QLineEdit()
        input2.setObjectName("poll_interval_input")
        input2.setFixedSize(450, 30)
        hbox_input2.addWidget(input2_label)
        hbox_input2.addWidget(input2)
        form_layout_left.addLayout(hbox_input2)

        settings_labels.append(input2_label)
        settings_inputs.append(input2)

        form_layout_right = QVBoxLayout()

        hbox_input3 = QHBoxLayout()
        input3_label = QLabel("Beförderung bis")
        input3_label.setFixedWidth(120)
        input3_label.setStyleSheet(label_children_style)
        input3 = QLineEdit()
        input3.setObjectName("befoerderung_bis_input")
        input3.setFixedSize(450, 30)
        hbox_input3.addWidget(input3_label)
        hbox_input3.addWidget(input3)
        form_layout_right.addLayout(hbox_input3)

        settings_labels.append(input3_label)
        settings_inputs.append(input3)

        hbox_input4 = QHBoxLayout()
        input4_label = QLabel("Escalation timeout")
        input4_label.setFixedWidth(120)
        input4_label.setStyleSheet(label_children_style)
        input4 = QLineEdit()
        input4.setObjectName("escalation_timeout_input")
        input4.setFixedSize(450, 30)
        hbox_input4.addWidget(input4_label)
        hbox_input4.addWidget(input4)
        form_layout_right.addLayout(hbox_input4)

        settings_labels.append(input4_label)
        settings_inputs.append(input4)

        polling_label.mousePressEvent = lambda event: toggle_inputs(settings_labels, settings_inputs)

        hbox_columns = QHBoxLayout()
        hbox_columns.addLayout(form_layout_left)
        hbox_columns.addStretch()
        hbox_columns.addLayout(form_layout_right)

        group_layout.addLayout(hbox_columns)

        group_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        hbox_new_settings = QHBoxLayout()
        new_label = QLabel("Compression")
        new_label.setStyleSheet(label_style)
        new_label.setFixedWidth(120)
        hbox_new_settings.addWidget(new_label)

        new_checkbox1 = QCheckBox("Pre-Unzip")
        new_checkbox1.setObjectName("pre_unzip_checkbox")
        new_checkbox1.setStyleSheet(checkbox_style)
        new_checkbox1.setFixedWidth(200)
        hbox_new_settings.addWidget(new_checkbox1)

        new_checkbox2 = QCheckBox("Post-Zip")
        new_checkbox2.setObjectName("post_zip_checkbox")
        new_checkbox2.setStyleSheet(checkbox_style)
        hbox_new_settings.addWidget(new_checkbox2)

        group_layout.addLayout(hbox_new_settings)

        group_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        hbox_additional_settings = QHBoxLayout()
        additional_label = ClickableLabel("Other Settings")
        additional_label.setStyleSheet(label_style)
        additional_label.setFixedWidth(120)
        hbox_additional_settings.addWidget(additional_label)

        additional_checkbox1 = QCheckBox("Rename with Timestamp")
        additional_checkbox1.setObjectName("rename_with_timestamp_checkbox")
        additional_checkbox1.setStyleSheet(checkbox_style)
        hbox_additional_settings.addWidget(additional_checkbox1)

        group_layout.addLayout(hbox_additional_settings)

        group_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        hbox_new_inputs = QHBoxLayout()

        vbox_left = QVBoxLayout()
        hbox_new_input1 = QHBoxLayout()
        new_input_label1 = QLabel("Gültig ab")
        hbox_new_input1.addItem(QSpacerItem(125, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))
        new_input_label1.setFixedWidth(100)
        new_input_label1.setStyleSheet(label_children_style)
        new_input1 = QLineEdit()
        new_input1.setObjectName("gueltig_ab_input")
        new_input1.setFixedSize(450, 30)
        hbox_new_input1.addWidget(new_input_label1)
        hbox_new_input1.addWidget(new_input1)
        vbox_left.addLayout(hbox_new_input1)

        other_settings_labels.append(new_input_label1)
        other_settings_inputs.append(new_input1)

        vbox_right = QVBoxLayout()
        hbox_new_input2 = QHBoxLayout()
        new_input_label2 = QLabel("Gültig bis")
        new_input_label2.setFixedWidth(120)
        new_input_label2.setStyleSheet(label_children_style)
        new_input2 = QLineEdit()
        new_input2.setObjectName("gueltig_bis_input")
        new_input2.setFixedSize(450, 30)
        hbox_new_input2.addWidget(new_input_label2)
        hbox_new_input2.addWidget(new_input2)
        vbox_right.addLayout(hbox_new_input2)

        other_settings_labels.append(new_input_label2)
        other_settings_inputs.append(new_input2)

        hbox_new_inputs.addLayout(vbox_left)
        hbox_new_inputs.addStretch()
        hbox_new_inputs.addLayout(vbox_right)

        group_layout.addLayout(hbox_new_inputs)

        additional_label.mousePressEvent = lambda event: toggle_inputs(other_settings_labels, other_settings_inputs)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("QFrame { background-color: black; color: black; }")
        layout.addWidget(line)

    # Pattern group
    elif group_name == "Pattern":
        label_style = "border: none; font-size: 14px;"
        form_layout_left = QFormLayout()
        form_layout_right = QFormLayout()

        group_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        hbox_left_column = QHBoxLayout()
        hbox_left_column.addItem(QSpacerItem(125, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))
        hbox_left_column.addLayout(form_layout_left)

        pattern_label1 = QLabel("findPattern")
        pattern_label1.setFixedWidth(100)
        pattern_label1.setStyleSheet(label_style)
        pattern_input1 = QLineEdit()
        pattern_input1.setObjectName("find_pattern_input")
        pattern_input1.setFixedSize(450, 30)
        form_layout_left.addRow(pattern_label1, pattern_input1)

        pattern_label2 = QLabel("quitPattern")
        pattern_label2.setFixedWidth(100)
        pattern_label2.setStyleSheet(label_style)
        pattern_input2 = QLineEdit()
        pattern_input2.setObjectName("quit_pattern_input")
        pattern_input2.setFixedSize(450, 30)
        form_layout_left.addRow(pattern_label2, pattern_input2)

        pattern_label3 = QLabel("ackPattern")
        pattern_label3.setFixedWidth(100)
        pattern_label3.setStyleSheet(label_style)
        pattern_input3 = QLineEdit()
        pattern_input3.setObjectName("ack_pattern_input")
        pattern_input3.setFixedSize(450, 30)
        form_layout_left.addRow(pattern_label3, pattern_input3)

        pattern_label4 = QLabel("zipPattern")
        pattern_label4.setFixedWidth(100)
        pattern_label4.setStyleSheet(label_style)
        pattern_input4 = QLineEdit()
        pattern_input4.setObjectName("zip_pattern_input")
        pattern_input4.setFixedSize(450, 30)
        form_layout_left.addRow(pattern_label4, pattern_input4)

        pattern_label5 = QLabel("movPattern")
        pattern_label5.setFixedWidth(120)
        pattern_label5.setStyleSheet(label_style)
        pattern_input5 = QLineEdit()
        pattern_input5.setObjectName("mov_pattern_input")
        pattern_input5.setFixedSize(450, 30)
        form_layout_right.addRow(pattern_label5, pattern_input5)

        pattern_label6 = QLabel("putPattern")
        pattern_label6.setFixedWidth(120)
        pattern_label6.setStyleSheet(label_style)
        pattern_input6 = QLineEdit()
        pattern_input6.setObjectName("put_pattern_input")
        pattern_input6.setFixedSize(450, 30)
        form_layout_right.addRow(pattern_label6, pattern_input6)

        pattern_label7 = QLabel("rcvPattern")
        pattern_label7.setFixedWidth(120)
        pattern_label7.setStyleSheet(label_style)
        pattern_input7 = QLineEdit()
        pattern_input7.setObjectName("rcv_pattern_input")
        pattern_input7.setFixedSize(450, 30)
        form_layout_right.addRow(pattern_label7, pattern_input7)

        hbox_columns = QHBoxLayout()
        hbox_columns.addLayout(hbox_left_column)
        hbox_columns.addStretch()
        hbox_columns.addLayout(form_layout_right)

        group_layout.addLayout(hbox_columns)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("QFrame { background-color: black; color: black; }")
        layout.addWidget(line)

    # PostCommand(s) group
    elif group_name == "PostCommand(s)":

        label_style = "border: none; font-size: 14px;"
        form_layout = QFormLayout()

        group_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        num_elements = 1

        for i in range(num_elements):
            vbox = QVBoxLayout()
            hbox = QHBoxLayout()
            label = QLabel(f"class ({i + 1})")
            label.setStyleSheet(label_style)
            label.setFixedWidth(100)
            input_field = QLineEdit()
            input_field.setFixedHeight(30)

            hbox_first_input = QHBoxLayout()
            hbox_first_input.addWidget(input_field)

            add_button_first = QPushButton("+")
            add_button_first.setObjectName("addButton")
            add_button_first.setStyleSheet("""
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
            add_button_first.setFixedSize(30, 30)
            remove_button_first = QPushButton("-")
            remove_button_first.setObjectName("removeButton")
            remove_button_first.setStyleSheet("""
                #removeButton {
                    background-color: #f0f0f0;
                    border: 1px solid #A9A9A9;
                    border-radius: 15px;
                    text-align: center;
                    font-size: 16px;
                    font-weight: bold;
                }
                
                #removeButton:hover {
                    background-color: #dcdcdc;
                    cursor: pointer;
                }
                
                #removeButton:pressed {
                    background-color: #c0c0c0;
                }
                """)
            remove_button_first.setFixedSize(30, 30)

            hbox_first_input.addWidget(add_button_first)
            hbox_first_input.addWidget(remove_button_first)

            hbox.addWidget(label)
            hbox.addLayout(hbox_first_input)
            vbox.addLayout(hbox)

            hbox_inputs = QHBoxLayout()
            input_field1 = QComboBox()
            hbox_inputs.addItem(QSpacerItem(106, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))
            input_field1.setFixedSize(450, 30)
            input_field2 = QLineEdit()
            input_field2.setFixedSize(450, 30)

            hbox_second_input = QHBoxLayout()
            hbox_second_input.addWidget(input_field2)

            add_button_second = QPushButton("+")
            add_button_second.setObjectName("addButton")
            add_button_second.setStyleSheet("""
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
            add_button_second.setFixedSize(30, 30)
            remove_button_second = QPushButton("-")
            remove_button_second.setObjectName("removeButton")
            remove_button_second.setStyleSheet("""
                #removeButton {
                    background-color: #f0f0f0;
                    border: 1px solid #A9A9A9;
                    border-radius: 15px;
                    text-align: center;
                    font-size: 16px;
                    font-weight: bold;
                }
                
                #removeButton:hover {
                    background-color: #dcdcdc;
                    cursor: pointer;
                }
                
                #removeButton:pressed {
                    background-color: #c0c0c0;
                }
                """)
            remove_button_second.setFixedSize(30, 30)

            hbox_second_input.addWidget(add_button_second)
            hbox_second_input.addWidget(remove_button_second)

            hbox_inputs.addWidget(input_field1)
            hbox_inputs.addStretch()
            hbox_inputs.addLayout(hbox_second_input)
            vbox.addLayout(hbox_inputs)

            form_layout.addRow(vbox)

        group_layout.addLayout(form_layout)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("QFrame { background-color: black; color: black; }")
        layout.addWidget(line)

    group_box.setLayout(group_layout)
    layout.addWidget(group_box)


# Toggle function
def toggle_inputs(labels, inputs):
    for label, input_field in zip(labels, inputs):
        if label.isVisible():
            label.hide()
            input_field.hide()
        else:
            label.show()
            input_field.show()


