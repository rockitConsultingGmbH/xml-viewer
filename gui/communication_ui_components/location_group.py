from PyQt5.QtWidgets import QLabel, QCheckBox, QLineEdit, QPushButton, QFormLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QWidget
from gui.communication_ui_components.target_location import TargetLocationForm
from gui.communication_ui_components.source_location import SourceLocationForm

class LocationsGroup(QWidget):
    def __init__(self, group_layout, communication_id, parent_widget=None):
        super().__init__(parent_widget)
        self.parent_widget = parent_widget
        self.group_layout = group_layout
        self.communication_id = communication_id


    def create_location_group(self):
        form_layout = QFormLayout()
        form_layout.setHorizontalSpacing(20)
        form_layout.setVerticalSpacing(15)

        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.group_layout.addItem(spacer)

        source_location_label = QLabel("Source Location")
        source_location_label.setObjectName("label_parent")
        self.group_layout.addWidget(source_location_label)

        # Source Location Form
        self.source_location_form = SourceLocationForm(self.communication_id)
        form_layout.addRow(self.source_location_form.setup_ui())

        spacer = QSpacerItem(0, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        form_layout.addItem(spacer)
        self.group_layout.addItem(spacer)

        # Target Location(s) Section
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

        # Target Location Form
        self.target_location_form = TargetLocationForm(self.communication_id)
        self.target_locations_form_layout = self.target_location_form.setup_ui()
        form_layout.addRow(self.target_locations_form_layout)

        self.group_layout.addLayout(form_layout)
        
        # Connect add button to add a new target location
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

    def reset_ui(self):
        self.target_location_form.reset_target_location_deletions()
        self.source_location_form.reset_source_location()

