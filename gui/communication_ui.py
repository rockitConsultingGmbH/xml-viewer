import logging
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QGroupBox, QScrollArea, QWidget, QFrame, QSpacerItem, QSizePolicy

from controllers.command_table_data import CommandParamTableData
from controllers.communication_table_data import CommunicationTableData
from controllers.description_table_data import DescriptionTableData
from controllers.location_table_data import LocationTableData

from gui.communication_ui_components.overview_group import OverviewGroup
from gui.communication_ui_components.patterns_group import PatternGroup
from gui.communication_ui_components.settings_group import SettingsGroup
from gui.communication_ui_components.location_group import LocationsGroup
from gui.communication_ui_components.commands_group import CommandsGroup

from gui.common_components.popup_message import PopupMessage
from gui.common_components.buttons import Buttons
from gui.common_components.toggle_inputs import toggle_inputs

from gui.common_components.stylesheet_loader import load_stylesheet

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class CommunicationUI(QWidget):
    name_updated = pyqtSignal(int, str)
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

        communications_box = QGroupBox("Communications")
        communications_box.setObjectName("group-border")
        self.communications_box_layout = QVBoxLayout()

        # Add spacer item
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.communications_box_layout.addItem(spacer)

        self.create_group("Overview", self.communications_box_layout, self.communication_id)
        self.create_group("Locations", self.communications_box_layout, self.communication_id)
        self.create_group("Settings", self.communications_box_layout)
        self.create_group("Pattern", self.communications_box_layout)
        self.create_group("Commands", self.communications_box_layout)

        communications_box.setLayout(self.communications_box_layout)
        scroll_layout.addWidget(communications_box)

        scroll_area.setWidget(scroll_content)

        layout = QVBoxLayout(self)
        button_layout = Buttons().create_button_layout(self)
        layout.addLayout(button_layout)
        layout.addWidget(scroll_area)
        self.setLayout(layout)

    def set_fields_from_db(self):
        if self.communication_id is not None:
            self.populate_fields_from_db()

    def populate_fields_from_db(self):
        if self.communication_id is not None:
            self.communication_table_data.populate_communication_table_fields(self.communication_id)
            self.descritpion_table_data.populate_description_fields(self.communication_id)
            self.location_table_data.populate_source_location_fields(self.communication_id)
            self.location_table_data.populate_target_location_fields(self.communication_id)
            self.commands_ui.refresh_commands_ui()

    def save_fields_to_db(self):
        try:
            if not self.name_input.text().strip():
                self.popup_message.show_error_message(f"Error while saving data...")
                return
            self.communication_table_data.save_communication_data(self.communication_id)
            new_name = self.communication_table_data.get_communication_name(self.communication_id)
            self.name_updated.emit(self.communication_id, new_name)

            self.descritpion_table_data.save_description_data(self.communication_id)
            self.location_table_data.save_source_location_data(self.communication_id)
            self.location_table_data.save_target_location_data(self.communication_id)
            self.commands_ui.save_commands()

            description_ids_to_delete = self.overview_group_instance.description_form.get_description_ids_to_delete()
            if description_ids_to_delete:
                self.descritpion_table_data.delete_description_data(description_ids_to_delete)

            target_location_ids_to_delete = self.location_group.targe_location_form.get_target_location_ids_to_delete()
            if target_location_ids_to_delete:
                self.location_table_data.delete_location_data(target_location_ids_to_delete)
            self.popup_message.show_message("Changes have been successfully saved.")

        except Exception as e:
            self.popup_message.show_error_message(f"Error while saving data: {e}")

    def create_group(self, group_name, layout, communication_id=None):
        group_box = QGroupBox(group_name)
        group_layout = QVBoxLayout()

        if group_name == "Overview":
            self.overview_group_instance = OverviewGroup(group_layout, self._communication_id)
            self.name_input = self.overview_group_instance.get_name_input()
            line = self.create_horizontal_line()
            group_layout.addWidget(line)

        elif group_name == "Locations":
            self.location_group = LocationsGroup(group_layout, self._communication_id, toggle_inputs)
            self.location_group.create_location_group()
            line = self.create_horizontal_line()
            group_layout.addWidget(line)

        elif group_name == "Settings":
            self.settings_group = SettingsGroup(group_layout, self._communication_id, toggle_inputs)
            self.settings_group.create_settings_group()
            line = self.create_horizontal_line()
            group_layout.addWidget(line)

        elif group_name == "Pattern":
            self.pattern_group = PatternGroup(group_layout, self._communication_id)
            self.pattern_group.create_pattern_group()
            line = self.create_horizontal_line()
            group_layout.addWidget(line)

        elif group_name == "Commands":
            self.commands_ui = CommandsGroup(self.communication_id)
            self.commands_ui.create_commands_group()
            group_layout.addWidget(self.commands_ui)

        group_box.setLayout(group_layout)
        layout.addWidget(group_box)

    @staticmethod
    def create_horizontal_line():
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setObjectName("divider-line")
        return line