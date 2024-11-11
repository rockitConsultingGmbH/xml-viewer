from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QCheckBox, QLineEdit, QPushButton, QFormLayout, QHBoxLayout, QSpacerItem, \
    QSizePolicy

from gui.communication_ui_components.descriptions import DescriptionForm

class OverviewGroup:
    def __init__(self, group_layout, communication_id):
        self.group_layout = group_layout
        self.communication_id = communication_id
        self.description_form = DescriptionForm(self.communication_id)
        self.setup_ui()

    def setup_ui(self):
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.group_layout.addItem(spacer)

        hbox1 = QHBoxLayout()

        #polling_status_label = QLabel("Polling aktiviert:")
        self.polling_status = QLabel()
        self.polling_status.setObjectName("polling_status")
        self.polling_status.setAlignment(Qt.AlignLeft)
        self.polling_status.setStyleSheet("font-weight: bold;")  
    
        description_label = QLabel("Description(s)")
        description_label.setFixedWidth(100)
        self.addButton = QPushButton("+")
        self.addButton.setFixedSize(30, 30)
        self.addButton.setObjectName("addButton")

        #hbox1.addWidget(polling_status_label)
        hbox1.addWidget(self.polling_status)
        hbox1.addWidget(description_label)
        hbox1.addWidget(self.addButton)

        hbox1.addSpacerItem(QSpacerItem(550, 20, QSizePolicy.Fixed, QSizePolicy.Minimum))

        self.group_layout.addLayout(hbox1)

        hbox_columns = QHBoxLayout()
        form_layout_left = QFormLayout()

        name_label = QLabel("Name")
        self.name_input = QLineEdit()
        self.name_input.setFixedSize(450, 30)
        self.name_input.setObjectName("name_input")
        form_layout_left.addRow(name_label, self.name_input)

        alt_name_label = QLabel("Alternate Namelist")
        self.alt_name_input = QLineEdit()
        self.alt_name_input.setObjectName("alt_name_input")
        self.alt_name_input.setFixedSize(400, 30)

        self.goButton = QPushButton("GO")
        self.goButton.setObjectName("goButton")
        self.goButton.setFixedSize(43, 30)
        self.goButton.setToolTip("Go to Alternate NameList...")
        self.goButton.setEnabled(False)

        hbox_alt_name = QHBoxLayout()
        hbox_alt_name.addWidget(self.alt_name_input)
        hbox_alt_name.addWidget(self.goButton)
        form_layout_left.addRow(alt_name_label, hbox_alt_name)

        hbox_columns.addLayout(form_layout_left)
        hbox_columns.addStretch(1)
        form_layout_right = self.description_form.get_form_layout()
        hbox_columns.addLayout(form_layout_right)

        self.group_layout.addLayout(hbox_columns)

        self.addButton.clicked.connect(lambda: self.description_form.add_description_fields({'id': 'new', 'description': ''}))

    def get_name_input(self):
        return self.name_input
