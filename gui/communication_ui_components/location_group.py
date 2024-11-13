from PyQt5.QtWidgets import QLabel, QCheckBox, QLineEdit, QPushButton, QFormLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QVBoxLayout, QWidget
from gui.common_components.clickable_label import ClickableLabel
from gui.communication_ui_components.target_location import TargetLocationForm

class LocationsGroup(QWidget):
    def __init__(self, group_layout, communication_id, toggle_inputs, parent=None):
        super().__init__(parent)
        self.group_layout = group_layout
        self.communication_id = communication_id
        self.toggle_inputs = toggle_inputs
        self.source_labels = []
        self.source_inputs = []
        self.source_checkboxes = []

    def create_location_group(self):
        form_layout = QFormLayout()
        form_layout.setHorizontalSpacing(20)
        form_layout.setVerticalSpacing(15)

        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.group_layout.addItem(spacer)

        source_location_label = QLabel("Source Location")
        source_location_label.setObjectName("label_parent")
        self.group_layout.addWidget(source_location_label)

        bottom_spacer = QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.group_layout.addItem(bottom_spacer)

        source_label = ClickableLabel("Source")
        source_label.setFixedWidth(70)
        source_label.setStyleSheet("font-weight: bold;")
        source_input = QLineEdit()
        source_input.setFixedHeight(30)
        source_input.setObjectName("source_input")

        form_layout.addRow(source_label, source_input)

        hbox_columns = QHBoxLayout()

        left_column_layout = QFormLayout()
        left_column_layout.setVerticalSpacing(15)

        userid_label = QLabel("User ID")
        userid_input = QLineEdit()
        userid_input.setObjectName("userid_source_input")
        userid_input.setFixedHeight(30)
        left_column_layout.addRow(userid_label, userid_input)

        location_id_label = QLabel("Location ID")
        location_id_label.setFixedWidth(100)
        location_id_input = QLineEdit()
        location_id_input.setObjectName("location_id_input")
        location_id_input.setFixedHeight(30)
        left_column_layout.addRow(location_id_label, location_id_input)

        right_column_layout = QFormLayout()
        right_column_layout.setVerticalSpacing(15)

        password_label = QLabel("Password")
        password_label.setFixedWidth(80)
        password_input = QLineEdit()
        password_input.setObjectName("password_source_input")
        password_input.setFixedHeight(30)
        right_column_layout.addRow(password_label, password_input)

        source_description_label = QLabel("Description")
        source_description_label.setFixedWidth(100)
        source_description_input = QLineEdit()
        source_description_input.setObjectName("source_description_input")
        source_description_input.setFixedHeight(30)
        right_column_layout.addRow(source_description_label, source_description_input)

        left_column_with_margin = QHBoxLayout()
        left_margin = QSpacerItem(90, 0, QSizePolicy.Fixed, QSizePolicy.Minimum)
        left_column_with_margin.addItem(left_margin)
        left_column_with_margin.addLayout(left_column_layout)
        hbox_columns.addLayout(left_column_with_margin)
        hbox_columns.addSpacing(50)
        hbox_columns.addLayout(right_column_layout)

        form_layout.addRow(hbox_columns)

        form_layout.addItem(QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        target_label = QLabel("Target Location(s)")
        target_label.setFixedWidth(145)
        target_label.setObjectName("label_parent")

        add_target_location_button = QPushButton("+")
        add_target_location_button.setFixedSize(30, 30)
        add_target_location_button.setObjectName("addButton")

        hbox_target = QHBoxLayout()
        hbox_target.addWidget(target_label)
        hbox_target.addWidget(add_target_location_button)

        form_layout.addRow(hbox_target)

        self.targe_location_form = TargetLocationForm(self.communication_id)
        self.target_locations_form_layout = self.targe_location_form.create_form()
        form_layout.addRow(self.target_locations_form_layout)

        self.group_layout.addLayout(form_layout)

        self.source_labels.extend([userid_label, location_id_label, password_label, source_description_label])
        self.source_inputs.extend([userid_input, location_id_input, password_input, source_description_input])

        source_label.mousePressEvent = lambda event: self.toggle_inputs(self.source_labels + self.source_checkboxes, self.source_inputs)

        add_target_location_button.clicked.connect(lambda: self.targe_location_form.add_target_location_fields({
            'id': 'new',
            'userid': '',
            'location_id': '',
            'location': '',
            'password': '',
            'description': '',
            'useLocalFilename': '',
            'usePathFromConfig': '',
            'renameExistingFile': ''
        }))

    def reset_ui(self):
        self.targe_location_form.reset_target_location_deletions()
