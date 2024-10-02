from PyQt5.QtWidgets import QVBoxLayout, QGroupBox, QHBoxLayout, QCheckBox, QPushButton, QLabel, \
    QLineEdit, QFormLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt


# Clickable Label class for transforming labels into clickable buttons
class ClickableLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)


# Group Builder
def setup_right_interface(right_widget):
    right_layout = QVBoxLayout()

    create_group("Overview", right_layout)
    create_group("Locations", right_layout)
    create_group("Settings", right_layout)
    create_group("Pattern", right_layout)
    create_group("PostCommands", right_layout)

    right_widget.setLayout(right_layout)


# Group interface builder
def create_group(group_name, layout):
    global input_labels, input_fields, source_labels, source_inputs, target_labels, target_inputs
    group_box = QGroupBox(group_name)
    group_box.setStyleSheet("QGroupBox { font-weight: bold; font-size: 15px; }")
    group_layout = QVBoxLayout()

    if group_name == "Overview":
        input_labels = []
        input_fields = []
    elif group_name == "Locations":
        source_labels = []
        source_inputs = []
        target_labels = []
        target_inputs = []

    # Overview group
    if group_name == "Overview":
        label_style = "border: none; font-size: 14px;"
        checkbox_style = "border: none;"

        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        group_layout.addItem(spacer)

        hbox1 = QHBoxLayout()
        checkbox = QCheckBox("Polling aktiviert")
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
        form_layout_left.addRow(name_label, name_input)

        alt_name_label = QLabel("Alternate Namelist")
        alt_name_label.setStyleSheet(label_style)
        alt_name_input = QLineEdit()
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
        description_label.mousePressEvent = lambda event: toggle_inputs(input_labels, input_fields)

        description_input = QLineEdit()
        description_input.setFixedSize(450, 30)

        form_layout_right.addRow(description_label, description_input)

        for i in range(3):
            input_label = QLabel(f"Description {i + 1}")
            input_label.setStyleSheet(label_style)
            input_field = QLineEdit()
            input_field.setFixedSize(450, 30)
            input_labels.append(input_label)
            input_fields.append(input_field)

            form_layout_right.addRow(input_label, input_field)
            input_label.hide()
            input_field.hide()

        hbox_columns.addLayout(form_layout_right)
        group_layout.addLayout(hbox_columns)


    # Locations group
    elif group_name == "Locations":
        label_style = "border: none; font-size: 14px;"
        form_layout = QFormLayout()
        form_layout.setHorizontalSpacing(10)
        form_layout.setVerticalSpacing(15)

        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        group_layout.addItem(spacer)

        # Source
        source_label = ClickableLabel("Source")
        source_label.setStyleSheet(label_style)
        source_input = QLineEdit()
        source_input.setFixedHeight(30)

        form_layout.addRow(source_label, source_input)

        hbox_userid_password = QHBoxLayout()

        hbox_userid_password.addSpacing(55)

        userid_label = QLabel("UserID")
        userid_label.setStyleSheet(label_style)
        userid_label.setFixedWidth(60)
        userid_input = QLineEdit()
        userid_input.setFixedSize(450, 30)

        password_label = QLabel("Password")
        password_label.setStyleSheet(label_style)
        password_label.setFixedWidth(80)
        password_input = QLineEdit()
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

        # Target Locations
        target_label = QLabel("Target Locations(s)")
        target_label.setFixedWidth(130)
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
                    font-size: 18px;
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

        target_count = 3
        for i in range(1, target_count + 1):
            target_label = ClickableLabel(f"Target({i})")
            target_label.setFixedWidth(130)
            target_label.setStyleSheet(label_style)

            target_input = QLineEdit()
            target_input.setFixedHeight(30)

            userid_target_label = QLabel("UserID")
            userid_target_label.setStyleSheet(label_style)
            userid_target_label.setFixedWidth(60)
            userid_target_input = QLineEdit()
            userid_target_input.setFixedSize(450, 30)

            password_target_label = QLabel("Password")
            password_target_label.setStyleSheet(label_style)
            password_target_label.setFixedWidth(80)
            password_target_input = QLineEdit()
            password_target_input.setFixedSize(450, 30)

            target_labels.append(userid_target_label)
            target_labels.append(password_target_label)
            target_inputs.append(userid_target_input)
            target_inputs.append(password_target_input)

            hbox_target_row = QHBoxLayout()
            hbox_target_row.addWidget(target_label)
            hbox_target_row.addWidget(target_input)

            hbox_userid_target_password_row = QHBoxLayout()
            hbox_userid_target_password_row.addWidget(userid_target_label)
            hbox_userid_target_password_row.addWidget(userid_target_input)
            hbox_userid_target_password_row.addStretch()
            hbox_userid_target_password_row.addWidget(password_target_label)
            hbox_userid_target_password_row.addWidget(password_target_input)

            form_layout.addRow(hbox_target_row)
            form_layout.addRow(hbox_userid_target_password_row)

            # Теперь делаем кликабельным каждый Target
            target_label.mousePressEvent = lambda event, labels=[userid_target_label, password_target_label],\
                                                  inputs=[userid_target_input, password_target_input]: toggle_inputs(
                labels, inputs)

        group_layout.addLayout(form_layout)

    group_box.setLayout(group_layout)
    layout.addWidget(group_box)

    # TODO Create a Settings group

# Toggle function
def toggle_inputs(labels, inputs):
    for label, input_field in zip(labels, inputs):
        if label.isVisible():
            label.hide()
            input_field.hide()
        else:
            label.show()
            input_field.show()
