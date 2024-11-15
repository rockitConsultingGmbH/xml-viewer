from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QFormLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QWidget
from common.connection_manager import ConnectionManager
from database.utils import select_from_location
from gui.common_components.icons import add_button_icon
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
        self.conn_manager = ConnectionManager()
        self.load_source_locations()
        self.target_location_form = TargetLocationForm(self.communication_id)

    def load_source_locations(self):
        self.conn = self.conn_manager.get_db_connection()
        self.cursor = self.conn.cursor()
        self.source_locations = select_from_location(self.cursor, self.communication_id, 'sourceLocation').fetchone()
        self.conn.close()

    def setup_ui(self):
        form_layout = QFormLayout()
        form_layout.setHorizontalSpacing(20)
        form_layout.setVerticalSpacing(15)

        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.group_layout.addItem(spacer)

        self.source_location_label = QLabel("Source Location")
        self.source_location_label.setObjectName("label_parent")
        self.group_layout.addWidget(self.source_location_label)

        bottom_spacer = QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.group_layout.addItem(bottom_spacer)

        self.source_label = ClickableLabel("Source")
        self.source_label.setFixedWidth(70)
        self.source_label.setStyleSheet("font-weight: bold;")
        self.source_input = QLineEdit()
        self.source_input.setFixedHeight(30)
        self.source_input.setObjectName("source_input")

        form_layout.addRow(self.source_label, self.source_input)

        hbox_columns = QHBoxLayout()

        left_column_layout = QFormLayout()
        left_column_layout.setVerticalSpacing(15)

        self.userid_label = QLabel("User ID")
        self.userid_input = QLineEdit()
        self.userid_input.setObjectName("userid_source_input")
        self.userid_input.setFixedHeight(30)
        left_column_layout.addRow(self.userid_label, self.userid_input)

        self.location_id_label = QLabel("Location ID")
        self.location_id_label.setFixedWidth(100)
        self.location_id_input = QLineEdit()
        self.location_id_input.setObjectName("location_id_input")
        self.location_id_input.setFixedHeight(30)
        left_column_layout.addRow(self.location_id_label, self.location_id_input)

        right_column_layout = QFormLayout()
        right_column_layout.setVerticalSpacing(15)

        self.password_label = QLabel("Password")
        self.password_label.setFixedWidth(80)
        self.password_input = QLineEdit()
        self.password_input.setObjectName("password_source_input")
        self.password_input.setFixedHeight(30)
        right_column_layout.addRow(self.password_label, self.password_input)

        self.source_description_label = QLabel("Description")
        self.source_description_label.setFixedWidth(100)
        self.source_description_input = QLineEdit()
        self.source_description_input.setObjectName("source_description_input")
        self.source_description_input.setFixedHeight(30)
        right_column_layout.addRow(self.source_description_label, self.source_description_input)

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

        add_target_location_button = QPushButton()
        add_target_location_button.setFixedSize(30, 30)
        add_target_location_button.setIcon(add_button_icon)
        add_target_location_button.setObjectName("addButton")

        hbox_target = QHBoxLayout()
        hbox_target.addWidget(target_label)
        hbox_target.addWidget(add_target_location_button)

        form_layout.addRow(hbox_target)

        self.target_locations_form_layout = self.target_location_form.setup_ui()
        form_layout.addRow(self.target_locations_form_layout)

        self.group_layout.addLayout(form_layout)

        self.source_labels.extend([self.userid_label, self.location_id_label, self.password_label, self.source_description_label])
        self.source_inputs.extend([self.userid_input, self.location_id_input, self.password_input, self.source_description_input])

        self.source_label.mousePressEvent = lambda event: self.toggle_inputs(self.source_labels + self.source_checkboxes, self.source_inputs)

        add_target_location_button.clicked.connect(lambda: self.target_location_form.add_target_location_fields({
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

        self.populate_fields(self.source_locations)

    def populate_fields(self, data):
        self.source_input.setText(data["location"])
        self.userid_input.setText(data["userid"])
        self.location_id_input.setText(data["location_id"])
        self.password_input.setText(data["password"])
        self.source_description_input.setText(data["description"])

    def reset_ui(self):
        self.populate_fields(self.source_locations)
        self.target_location_form.reset_target_location_deletions()