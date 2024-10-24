from PyQt5.QtWidgets import QLabel, QCheckBox, QLineEdit, QPushButton, QFormLayout, QHBoxLayout, QSpacerItem, \
    QSizePolicy

from gui.communication_ui_components.descriptions import DescriptionForm


def create_overview_group(group_layout, communication_id):

    spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
    group_layout.addItem(spacer)

    hbox1 = QHBoxLayout()
    checkbox = QCheckBox("Polling aktiviert")
    checkbox.setObjectName("polling_activate_checkbox")

    description_label = QLabel("Description(s)")
    description_label.setFixedWidth(100)
    add_descriptions_button = QPushButton("+")
    add_descriptions_button.setFixedSize(30, 30)
    add_descriptions_button.setObjectName("addButton")

    hbox1.addWidget(checkbox)
    hbox1.addWidget(description_label)
    hbox1.addWidget(add_descriptions_button)

    hbox1.addSpacerItem(QSpacerItem(510, 20, QSizePolicy.Fixed, QSizePolicy.Minimum))  # Spacer

    group_layout.addLayout(hbox1)

    hbox_columns = QHBoxLayout()

    form_layout_left = QFormLayout()

    name_label = QLabel("Name")
    name_input = QLineEdit()
    name_input.setFixedSize(450, 30)
    name_input.setObjectName("name_input")
    form_layout_left.addRow(name_label, name_input)

    alt_name_label = QLabel("Alternate Namelist")
    alt_name_input = QLineEdit()
    alt_name_input.setObjectName("alt_name_input")
    alt_name_input.setFixedSize(400, 30)

    go_button = QPushButton("GO")
    go_button.setObjectName("goButton")
    go_button.setFixedSize(43, 30)

    hbox_alt_name = QHBoxLayout()
    hbox_alt_name.addWidget(alt_name_input)
    hbox_alt_name.addWidget(go_button)
    form_layout_left.addRow(alt_name_label, hbox_alt_name)

    hbox_columns.addLayout(form_layout_left)
    hbox_columns.addStretch(1)

    description_form = DescriptionForm(communication_id)
    form_layout_right = description_form.create_description_form()
    hbox_columns.addLayout(form_layout_right)

    group_layout.addLayout(hbox_columns)

    add_descriptions_button.clicked.connect(lambda: description_form.add_description_fields(form_layout_right, {'id': 'new', 'description': ''}))