# post_command_group.py

from PyQt5.QtWidgets import QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QFormLayout, QComboBox, QPushButton, \
    QSpacerItem, QSizePolicy, QFrame


def create_post_command_group(group_layout):
    label_style = "border: none; font-size: 14px;"
    form_layout = QFormLayout()

    group_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

    num_elements = 1

    for i in range(num_elements):
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()

        # Creating the label and input field for class
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
