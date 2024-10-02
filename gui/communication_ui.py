from PyQt5.QtWidgets import QVBoxLayout, QGroupBox, QHBoxLayout, QCheckBox, QPushButton, QLabel, \
    QLineEdit, QFormLayout


def setup_right_interface(right_widget):
    right_layout = QVBoxLayout()

    create_group("Overview", right_layout)
    create_group("Locations", right_layout)
    create_group("Settings", right_layout)
    create_group("Pattern", right_layout)
    create_group("PostCommands", right_layout)

    right_widget.setLayout(right_layout)


def create_group(group_name, layout):
    group_box = QGroupBox(group_name)
    group_box.setStyleSheet("QGroupBox { font-weight: bold; font-size: 15px; }")
    group_layout = QVBoxLayout()

    if group_name == "Overview":
        label_style = "border: none;"
        checkbox_style = "border: none;"

        hbox1 = QHBoxLayout()
        checkbox = QCheckBox("Polling aktiviert")
        checkbox.setStyleSheet(checkbox_style)
        hbox1.addWidget(checkbox)
        hbox1.addStretch()

        reset_button = QPushButton("Reset")
        reset_button.setStyleSheet("background-color: red; color: white;")
        reset_button.setMinimumSize(80, 30)
        hbox1.addWidget(reset_button)

        save_button = QPushButton("Save")
        save_button.setStyleSheet("background-color: #2C3E50; color: white;")
        save_button.setMinimumSize(80, 30)
        hbox1.addWidget(save_button)

        group_layout.addLayout(hbox1)

        hbox_main = QHBoxLayout()

        vbox_form = QVBoxLayout()

        hbox_name = QHBoxLayout()
        name_label = QLabel("Name")
        name_label.setStyleSheet(label_style)
        name_input = QLineEdit()
        name_input.setFixedSize(300, 30)
        hbox_name.addWidget(name_label)
        hbox_name.addWidget(name_input)
        vbox_form.addLayout(hbox_name)

        hbox_alt_name = QHBoxLayout()
        alt_name_label = QLabel("Alternate Namelist")
        alt_name_label.setStyleSheet(label_style)
        alt_name_input = QLineEdit()
        alt_name_input.setFixedSize(250, 30)
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
        hbox_alt_name.addWidget(alt_name_label)
        hbox_alt_name.addWidget(alt_name_input)
        hbox_alt_name.addWidget(go_button)
        vbox_form.addLayout(hbox_alt_name)

        hbox_main.addLayout(vbox_form)

        vbox_desc = QVBoxLayout()
        hbox_desc_main = QHBoxLayout()
        desc_label_main = QLabel("Description(s)")
        desc_label_main.setStyleSheet(label_style)

        toggle_button = QPushButton("Toggle")
        toggle_button.setObjectName("toggleButton")
        toggle_button.setFixedSize(60, 30)
        toggle_button.setStyleSheet("""
            #toggleButton {
                background-color: #f0f0f0;
                border: 1px solid #A9A9A9;
            }
            #toggleButton:hover {
                background-color: #dcdcdc;
                cursor: pointer;
            }
            #toggleButton:pressed {
                background-color: #c0c0c0;
            }
        """)

        desc_input_main = QLineEdit()
        desc_input_main.setFixedSize(300, 30)

        hbox_desc_main.addWidget(desc_label_main)
        hbox_desc_main.addWidget(toggle_button)
        hbox_desc_main.addWidget(desc_input_main)

        vbox_desc.addLayout(hbox_desc_main)

        desc_widgets = []
        for i in range(1, 4):
            hbox_desc = QHBoxLayout()
            hbox_desc.setSpacing(0)
            desc_label = QLabel(f"Description {i}")
            desc_label.setStyleSheet(label_style)
            desc_input = QLineEdit()
            desc_input.setFixedSize(300, 30)
            hbox_desc.addWidget(desc_label)
            hbox_desc.addWidget(desc_input)
            vbox_desc.addLayout(hbox_desc)
            desc_widgets.append((desc_label, desc_input))

        toggle_button.clicked.connect(lambda: toggle_visibility(desc_widgets))

        hbox_main.addLayout(vbox_desc)
        group_layout.addLayout(hbox_main)

    group_box.setLayout(group_layout)
    layout.addWidget(group_box)


def toggle_visibility(widgets):
    for label, input in widgets:
        label.setVisible(not label.isVisible())
        input.setVisible(not input.isVisible())