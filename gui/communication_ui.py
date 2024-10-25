from PyQt5.QtWidgets import QVBoxLayout, QGroupBox, QScrollArea, QWidget, QFrame, QSpacerItem, QSizePolicy

from controllers.communication_table_data import save_communication_data, populate_communication_table_fields
from controllers.description_table_data import save_description_data, populate_description_fields
from controllers.location_table_data import save_source_location_data, save_target_location_data, \
    populate_location_target_fields, populate_location_source_fields
from gui.common_components.buttons import ButtonFactory
from gui.common_components.stylesheet_loader import load_stylesheet
from gui.common_components.toggle_inputs import toggle_inputs
from gui.communication_ui_components.overview_group import create_overview_group
from gui.communication_ui_components.patterns_group import create_pattern_group
from gui.communication_ui_components.settings_group import create_settings_group
from gui.communication_ui_components.source_location import create_locations_group
from gui.communication_ui_components.commands import CommandsUI


class CommunicationUI:
    def __init__(self, right_widget, communication_id):
        self.right_widget = right_widget
        self.communication_id = communication_id
        self.setup_right_interface()

        load_stylesheet(self.right_widget, "css/right_widget_styling.qss")

    def setup_right_interface(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        button_layout = ButtonFactory().create_button_layout(self)

        main_group_box = QGroupBox("Communications")
        main_group_box.setObjectName("group-border")
        main_group_layout = QVBoxLayout(main_group_box)

        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        main_group_layout.addItem(spacer)

        self.create_group("Overview", main_group_layout, self.communication_id)
        self.create_group("Locations", main_group_layout, self.communication_id)
        self.create_group("Settings", main_group_layout)
        self.create_group("Pattern", main_group_layout)
        self.create_group("PostCommand(s)", main_group_layout)

        scroll_layout.addLayout(button_layout)
        scroll_layout.addWidget(main_group_box)
        scroll_area.setWidget(scroll_content)

        right_layout = QVBoxLayout(self.right_widget)
        right_layout.addWidget(scroll_area)
        self.right_widget.setLayout(right_layout)

    def set_fields_from_db(self):
        populate_communication_table_fields(self.communication_id)
        populate_location_target_fields(self.communication_id)
        populate_description_fields(self.communication_id)
        populate_location_source_fields(self.communication_id)

    def save_fields_to_db(self):
        save_communication_data(self.communication_id)
        save_source_location_data(self.communication_id)
        save_target_location_data(self.communication_id)
        save_description_data(self.communication_id)

    def create_group(self, group_name, layout, communication_id=None):
        group_box = QGroupBox(group_name)
        group_layout = QVBoxLayout()

        if group_name == "Overview":
            create_overview_group(group_layout, communication_id)
            line = self.create_horizontal_line()
            group_layout.addWidget(line)

        elif group_name == "Locations":
            source_labels, source_inputs, source_checkboxes = [], [], []
            create_locations_group(group_layout, communication_id, toggle_inputs, source_labels, source_inputs,
                                   source_checkboxes)
            line = self.create_horizontal_line()
            group_layout.addWidget(line)

        elif group_name == "Settings":
            settings_labels, settings_inputs = [], []
            other_settings_labels, other_settings_inputs = [], []
            create_settings_group(group_layout, settings_labels, settings_inputs, other_settings_labels,
                                  other_settings_inputs, toggle_inputs)
            line = self.create_horizontal_line()
            group_layout.addWidget(line)

        elif group_name == "Pattern":
            create_pattern_group(group_layout)
            line = self.create_horizontal_line()
            group_layout.addWidget(line)

        elif group_name == "PostCommand(s)":
            commands_ui = CommandsUI()
            commands_ui.generate_send_tks_a_satz()
            # commands_ui.generate_tks_send()
            # commands_ui.generate_mq_put()
            # commands_ui.generate_execute()
            # commands_ui.generate_change_dsn_output()
            group_layout.addWidget(commands_ui)

        group_box.setLayout(group_layout)
        layout.addWidget(group_box)

    @staticmethod
    def create_horizontal_line():
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setObjectName("divider-line")
        return line