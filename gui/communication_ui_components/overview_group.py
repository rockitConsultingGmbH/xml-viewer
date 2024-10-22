from PyQt5.QtWidgets import QLabel, QCheckBox, QLineEdit, QPushButton, QFormLayout, QHBoxLayout, QSpacerItem, \
    QSizePolicy

from gui.communication_ui_components.descriptions import create_description_form, add_description_fields


# Modify the create_overview_group function
def create_overview_group(group_layout, communication_id):
    label_style = "border: none; font-size: 14px;"
    checkbox_style = "border: none;"

    spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
    group_layout.addItem(spacer)

    hbox1 = QHBoxLayout()
    checkbox = QCheckBox("Polling aktiviert")
    checkbox.setObjectName("polling_activate_checkbox")
    checkbox.setStyleSheet(checkbox_style)

    description_label = QLabel("Description(s)")
    description_label.setFixedWidth(90)
    description_label.setStyleSheet(label_style)
    add_descriptions_button = QPushButton("+")
    add_descriptions_button.setFixedSize(30, 30)
    add_descriptions_button.setObjectName("addButton")
    add_descriptions_button.setStyleSheet("""
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

    hbox1.addWidget(checkbox)
    hbox1.addWidget(description_label)
    hbox1.addWidget(add_descriptions_button)

    hbox1.addSpacerItem(QSpacerItem(510, 20, QSizePolicy.Fixed, QSizePolicy.Minimum))  # Spacer

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

    form_layout_right = create_description_form(label_style, communication_id)
    hbox_columns.addLayout(form_layout_right)

    group_layout.addLayout(hbox_columns)

    add_descriptions_button.clicked.connect(lambda: add_description_fields(form_layout_right, label_style, {'id': 'new', 'description': ''}))