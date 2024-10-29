from PyQt5.QtWidgets import QVBoxLayout, QGroupBox, QScrollArea, QWidget, QFrame, QHBoxLayout

from controllers.command_table_data import CommandParamTableData
from controllers.communication_table_data import CommunicationTableData
from controllers.description_table_data import DescriptionTableData
from controllers.location_table_data import LocationTableData

from gui.communication_ui_components.overview_group import OverviewGroup
from gui.communication_ui_components.patterns_group import create_pattern_group
from gui.communication_ui_components.settings_group import create_settings_group
from gui.communication_ui_components.source_location import create_locations_group
from gui.communication_ui_components.commands import CommandsUI

from gui.common_components.popup_message import PopupMessage
from gui.common_components.buttons import Buttons
from gui.common_components.toggle_inputs import toggle_inputs

from gui.common_components.stylesheet_loader import load_stylesheet

class CommunicationUI(QWidget):
    def __init__(self, communication_id, parent=None):
        super().__init__(parent)
        self._communication_id = communication_id

        self.popup_message = PopupMessage(self)
        self.communication_table_data = CommunicationTableData(self)
        self.descritpion_table_data = DescriptionTableData(self)
        self.location_table_data = LocationTableData(self)
        self.commandparam_table_data = CommandParamTableData(self)
        self.setup_ui()

        load_stylesheet(self, "css/right_widget_styling.qss")

    @property
    def communication_id(self):
            return self._communication_id

    def setup_ui(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        button_layout = Buttons().create_button_layout(self)
        communication_label_group = QGroupBox("Communication")
        communication_label_group.setFixedWidth(200)
        communication_label_group.setObjectName("communication-label-group")

        # Create a horizontal layout to place communication label group and buttons on the same level
        top_layout = QHBoxLayout()
        top_layout.addWidget(communication_label_group)
        top_layout.addLayout(button_layout)

        scroll_layout.addLayout(top_layout)

        self.create_group("Overview", scroll_layout, self.communication_id)
        self.create_group("Locations", scroll_layout, self.communication_id)
        self.create_group("Settings", scroll_layout)
        self.create_group("Pattern", scroll_layout)
        self.create_group("Commands", scroll_layout)

        scroll_area.setWidget(scroll_content)

        layout = QVBoxLayout(self)
        layout.addWidget(scroll_area)
        self.setLayout(layout)

    def set_fields_from_db(self):
        self.populate_fields_from_db()

    def populate_fields_from_db(self):
        self.communication_table_data.populate_communication_table_fields(self.communication_id)
        self.descritpion_table_data.populate_description_fields(self.communication_id)
        self.location_table_data.populate_source_location_fields(self.communication_id)
        self.location_table_data.populate_target_location_fields(self.communication_id)
        #self.location_table_data.populate_command_fields(self.communication_id)


    def save_fields_to_db(self):
        try:
            self.communication_table_data.save_communication_data(self.communication_id)
            self.descritpion_table_data.save_description_data(self.communication_id)
            self.location_table_data.save_source_location_data(self.communication_id)
            self.location_table_data.save_target_location_data(self.communication_id)
            self.commandparam_table_data.save_command_params(self.communication_id)
            #self.popup_message.show_message("Changes have been successfully saved.")
        except Exception as e:
            self.popup_message.show_error_message(f"Error while saving data: {e}")

    def create_group(self, group_name, layout, communication_id=None):
        group_box = QGroupBox(group_name)
        group_layout = QVBoxLayout()

        if group_name == "Overview":
            OverviewGroup(group_layout, communication_id)
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

        elif group_name == "Commands":
            commands_ui = CommandsUI(self.communication_id)
            commands_ui.generate_command_ui()
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