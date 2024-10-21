from PyQt5.QtWidgets import QMessageBox, QVBoxLayout, QGroupBox, QHBoxLayout, QPushButton, QScrollArea, QWidget, QFrame

from controllers.communication_table_data import save_communication_data
from controllers.description_table_data import save_description_data
from controllers.location_table_data import save_source_location_data, save_target_location_data

from gui.communication_ui_components.overview_group import create_overview_group
from gui.communication_ui_components.patterns_group import create_pattern_group
from gui.communication_ui_components.post_command_group import create_post_command_group
from gui.communication_ui_components.settings_group import create_settings_group
from gui.communication_ui_components.source_location import create_locations_group

from utils.toggle_inputs import toggle_inputs


class CommunicationUI:
    def __init__(self, right_widget, communication_id):
        self.right_widget = right_widget
        self.communication_id = communication_id
        self.setup_interface()

    def setup_interface(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; } QWidget { border: none; } "
                                  "QLineEdit, QComboBox, QPushButton { border: 1px solid gray; }")

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.create_reset_button(button_layout)
        self.create_save_button(button_layout)

        scroll_layout.addLayout(button_layout)

        self.create_group("Overview", scroll_layout, self.communication_id)
        self.create_group("Locations", scroll_layout, self.communication_id)
        self.create_group("Settings", scroll_layout)
        self.create_group("Pattern", scroll_layout)
        self.create_group("PostCommand(s)", scroll_layout)

        scroll_area.setWidget(scroll_content)

        right_layout = QVBoxLayout(self.right_widget)
        right_layout.addWidget(scroll_area)
        self.right_widget.setLayout(right_layout)

    def create_save_button(self, layout):
        save_button = QPushButton("Save")
        save_button.setFixedSize(100, 30)
        save_button.setObjectName("saveButton")
        save_button.setStyleSheet("""
            #saveButton {
                background-color: #db0d0d; color: white;
            }

            #saveButton:hover {
                background-color: #b00c0c;
            }

            #saveButton:pressed {
                background-color: #910909;
            }
        """)

        save_button.clicked.connect(self.save_and_show_message)
        layout.addWidget(save_button)

    def save_and_show_message(self):
        save_communication_data(self.communication_id)
        save_source_location_data(self.communication_id)
        save_target_location_data(self.communication_id)
        save_description_data(self.communication_id)

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Changes in Communication have been successfully saved.")
        msg.setWindowTitle("Save Successful")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def create_group(self, group_name, layout, communication_id=None):
        group_box = QGroupBox(group_name)
        group_box.setStyleSheet("QGroupBox { font-weight: bold; font-size: 15px; border: none; }")
        group_layout = QVBoxLayout()

        if group_name == "Overview":
            create_overview_group(group_layout, communication_id)
        elif group_name == "Locations":
            create_locations_group(group_layout, communication_id)
        elif group_name == "Settings":
            settings_labels, settings_inputs = [], []
            other_settings_labels, other_settings_inputs = [], []
            create_settings_group(group_layout, settings_labels, settings_inputs, other_settings_labels,
                                  other_settings_inputs, toggle_inputs)
        elif group_name == "Pattern":
            create_pattern_group(group_layout)
        elif group_name == "PostCommand(s)":
            create_post_command_group(group_layout)

        line = self.create_horizontal_line()
        group_layout.addWidget(line)

        group_box.setLayout(group_layout)
        layout.addWidget(group_box)

    @staticmethod
    def create_reset_button(layout):
        reset_button = QPushButton("Reset")
        reset_button.setFixedSize(100, 30)
        reset_button.setObjectName("resetButton")
        reset_button.setStyleSheet("""
            #resetButton {
                background-color: #9c9c9c; color: white;
            }

            #resetButton:hover {
                background-color: #8c8c8c;
            }

            #resetButton:pressed {
                background-color: #2d2d33;
            }
        """)
        layout.addWidget(reset_button)

    @staticmethod
    def create_horizontal_line():
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("QFrame { background-color: black; color: black; }")
        return line
