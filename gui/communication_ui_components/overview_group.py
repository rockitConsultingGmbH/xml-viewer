from PyQt5.QtWidgets import QLabel, QCheckBox, QLineEdit, QPushButton, QFormLayout, QHBoxLayout, QSpacerItem, \
    QSizePolicy

from gui.communication_ui_components.descriptions import create_description_form


def create_overview_group(group_layout, communication_id):
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

    form_layout_right = create_description_form(label_style, communication_id)
    hbox_columns.addLayout(form_layout_right)

    group_layout.addLayout(hbox_columns)
