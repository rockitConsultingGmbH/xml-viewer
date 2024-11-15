import logging
from PyQt5.QtWidgets import (QVBoxLayout, QFormLayout, QCheckBox,
                             QLineEdit, QWidget, QGroupBox, QSizePolicy, QSpacerItem)
from PyQt5.QtGui import QFont
from common.config_manager import ConfigManager
from common.connection_manager import ConnectionManager
from database.utils import select_from_basicconfig, update_basicconfig
from gui.common_components.popup_message import PopupMessage
from gui.common_components.buttons import Buttons
import sqlite3

from gui.common_components.stylesheet_loader import load_stylesheet

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class BasicConfigurationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.conn_manager = ConnectionManager()
        self.config_manager = ConfigManager()
        self.popup_message = PopupMessage(self)
        self.setup_ui()

        load_stylesheet(self, "css/right_widget_styling.qss")

    def setup_ui(self):
        basic_config_group = self.create_basic_config_group()
        layout = QVBoxLayout(self)
        button_layout = Buttons().create_button_layout(self)

        layout.addLayout(button_layout)
        layout.addWidget(basic_config_group)
        self.setLayout(layout)

    def create_basic_config_group(self):
        basic_config_group = QGroupBox("Basic Configuration")
        basic_config_group.setObjectName("group-border")
        form_layout = QFormLayout()

        self.init_input_fields()
        self.set_fields_from_db()

        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        form_layout.addItem(spacer)

        self.add_fields_to_form_layout(form_layout)

        basic_config_group.setLayout(form_layout)
        return basic_config_group

    def init_input_fields(self):
        self.stage_input = QLineEdit()
        self.temp_dir_input = QLineEdit()
        self.temp_dir1_input = QLineEdit()
        self.temp_dir2_input = QLineEdit()
        self.history_file_input = QLineEdit()
        self.history_file1_input = QLineEdit()
        self.history_file2_input = QLineEdit()
        self.already_transferred_file_input = QLineEdit()
        self.history_days_input = QLineEdit()
        self.archiver_time_input = QLineEdit()
        self.watcher_escalation_timeout_input = QLineEdit()
        self.watcher_sleep_time_input = QLineEdit()

        self.set_input_field_sizes()

    def set_input_field_sizes(self):
        large_fields = [
            self.temp_dir_input, self.temp_dir1_input, self.temp_dir2_input, 
            self.history_file_input, self.history_file1_input, self.history_file2_input, self.already_transferred_file_input
        ]
        small_fields = [
            self.stage_input, self.history_days_input, self.archiver_time_input, 
            self.watcher_escalation_timeout_input, self.watcher_sleep_time_input
        ]

        for field in large_fields + small_fields:
            field.setFixedSize(500, 35)

    def add_fields_to_form_layout(self, form_layout):
        fields = [
            ("Stage:", self.stage_input),
            ("Temp Dir:", self.temp_dir_input),
            ("Temp Dir 1:", self.temp_dir1_input),
            ("Temp Dir 2:", self.temp_dir2_input),
            ("History File:", self.history_file_input),
            ("History File 1:", self.history_file1_input),
            ("History File 2:", self.history_file2_input),
            ("Already Transferred File:", self.already_transferred_file_input),
            ("History Days:", self.history_days_input),
            ("Archiver Time:", self.archiver_time_input),
            ("Watcher Escalation Timeout:", self.watcher_escalation_timeout_input),
            ("Watcher Sleep Time:", self.watcher_sleep_time_input)
        ]

        for label, field in fields:
            form_layout.addRow(label, field)

    def set_fields_from_db(self):
        try:
            data = self.get_basic_configuration()
            if data:
                self.stage_input.setText(data["stage"])
                self.temp_dir_input.setText(data["tempDir"])
                self.temp_dir1_input.setText(data["tempDir1"])
                self.temp_dir2_input.setText(data["tempDir2"])
                self.history_file_input.setText(data["historyFile"])
                self.history_file1_input.setText(data["historyFile1"])
                self.history_file2_input.setText(data["historyFile2"])
                self.already_transferred_file_input.setText(data["alreadyTransferedFile"])
                self.history_days_input.setText(data["historyDays"])
                self.archiver_time_input.setText(data["archiverTime"])
                self.watcher_escalation_timeout_input.setText(data["watcherEscalationTimeout"])
                self.watcher_sleep_time_input.setText(data["watcherSleepTime"])
        except sqlite3.Error as e:
            self.popup_message.show_error_message(f"Error loading configuration: {e}")

    def get_basic_configuration(self):
        try:
            conn = self.conn_manager.get_db_connection()
            cursor = conn.cursor()
            select_from_basicconfig(cursor, self.config_manager.config_id)
            row = cursor.fetchone()
            conn.close()
            return row if row else None
        except Exception as e:
            logging.debug(f"Error while saving data: {e}")
            conn.rollback()
            self.popup_message.show_error_message(f"Error while saving data: {e}")
        finally:
            conn.close()

    def save_fields_to_db(self):
        row = {
            'id': self.config_manager.config_id,
            'stage': self.stage_input.text(),
            'tempDir': self.temp_dir_input.text(),
            'tempDir1': self.temp_dir1_input.text(),
            'tempDir2': self.temp_dir2_input.text(),
            'historyFile': self.history_file_input.text(),
            'historyFile1': self.history_file1_input.text(),
            'historyFile2': self.history_file2_input.text(),
            'alreadyTransferedFile': self.already_transferred_file_input.text(),
            'historyDays': self.history_days_input.text(),
            'archiverTime': self.archiver_time_input.text(),
            'watcherEscalationTimeout': self.watcher_escalation_timeout_input.text(),
            'watcherSleepTime': self.watcher_sleep_time_input.text()
        }

        try:
            conn = self.conn_manager.get_db_connection()
            cursor = conn.cursor()
            update_basicconfig(cursor, row)
            conn.commit()
            conn.close()
            self.popup_message.show_message("Changes have been successfully saved.")
        except Exception as e:
            logging.debug(f"Error while saving data: {e}")
            conn.rollback()
            self.popup_message.show_error_message(f"Error while saving data: {e}")
        finally:
            conn.close()
        
