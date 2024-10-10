from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QFormLayout, QCheckBox, QPushButton, 
                             QLineEdit, QWidget)
from PyQt5.QtCore import Qt

from common import config_manager
from database.connection_manager import ConnectionManager
from database.xml_to_db import get_db_connection
from gui.popup_message_ui import PopupMessage


class BasicConfigurationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.conn_manager = ConnectionManager()
        self.setup_ui()
        self.popup_message = PopupMessage(self)

    def setup_ui(self):
        # Main layout
        layout = QVBoxLayout(self)

        # Button layout
        button_layout = self.create_button_layout()

        # Form layout for input fields
        form_layout = QFormLayout()
        self.init_input_fields()
        self.populate_fields_from_db()
        self.add_fields_to_form_layout(form_layout)

        # Add layouts to the main layout
        layout.addLayout(button_layout)
        layout.addLayout(form_layout)
        self.setLayout(layout)

    def create_button_layout(self):
        # Creates and configures the Save and Reset buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        reset_button = QPushButton("Reset")
        reset_button.setFixedSize(100, 30)
        reset_button.setStyleSheet("background-color: #960e0e; color: white;")
        reset_button.clicked.connect(self.populate_fields_from_db)

        save_button = QPushButton("Save")
        save_button.setFixedSize(100, 30)
        save_button.setStyleSheet("background-color: #41414a; color: white;")
        save_button.clicked.connect(self.save_fields_to_db)

        button_layout.addWidget(reset_button)
        button_layout.addWidget(save_button)
        
        return button_layout

    def init_input_fields(self):
        # Initialize all input fields
        self.stage_input = QLineEdit()
        self.temp_dir_input = QLineEdit()
        self.temp_dir1_input = QLineEdit()
        self.temp_dir2_input = QLineEdit()
        self.history_file_input = QLineEdit()
        self.history_file1_input = QLineEdit()
        self.history_file2_input = QLineEdit()
        self.already_transferred_file_input = QCheckBox()
        self.history_days_input = QLineEdit()
        self.archiver_time_input = QLineEdit()
        self.watcher_escalation_timeout_input = QLineEdit()
        self.watcher_sleep_time_input = QLineEdit()

        # Set input field sizes
        self.set_input_field_sizes()

    def set_input_field_sizes(self):
        # Configures fixed sizes for input fields
        large_fields = [
            self.temp_dir_input, self.temp_dir1_input, self.temp_dir2_input, 
            self.history_file_input, self.history_file1_input, self.history_file2_input
        ]
        small_fields = [
            self.stage_input, self.history_days_input, self.archiver_time_input, 
            self.watcher_escalation_timeout_input, self.watcher_sleep_time_input
        ]

        for field in large_fields:
            field.setFixedSize(500, 35)
        for field in small_fields:
            field.setFixedSize(100, 35)

    def add_fields_to_form_layout(self, form_layout):
        # Adds input fields to the form layout with labels
        form_layout.addRow("Stage:", self.stage_input)
        form_layout.addRow("Temp Dir:", self.temp_dir_input)
        form_layout.addRow("Temp Dir 1:", self.temp_dir1_input)
        form_layout.addRow("Temp Dir 2:", self.temp_dir2_input)
        form_layout.addRow("History File:", self.history_file_input)
        form_layout.addRow("History File 1:", self.history_file1_input)
        form_layout.addRow("History File 2:", self.history_file2_input)
        form_layout.addRow("Already Transferred File:", self.already_transferred_file_input)
        form_layout.addRow("History Days:", self.history_days_input)
        form_layout.addRow("Archiver Time:", self.archiver_time_input)
        form_layout.addRow("Watcher Escalation Timeout:", self.watcher_escalation_timeout_input)
        form_layout.addRow("Watcher Sleep Time:", self.watcher_sleep_time_input)

    def populate_fields_from_db(self):
        # Retrieve and populate fields from database
        data = self.get_basic_configuration()
        if data:
            self.stage_input.setText(data[0])
            self.temp_dir_input.setText(data[1])
            self.temp_dir1_input.setText(data[2])
            self.temp_dir2_input.setText(data[3])
            self.history_file_input.setText(data[4])
            self.history_file1_input.setText(data[5])
            self.history_file2_input.setText(data[6])
            self.already_transferred_file_input.setChecked(data[7] == "true")
            self.history_days_input.setText(data[8])
            self.archiver_time_input.setText(data[9])
            self.watcher_escalation_timeout_input.setText(data[10])
            self.watcher_sleep_time_input.setText(data[11])

    def get_basic_configuration(self):
        # Fetch configuration data from the database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT stage, tempDir, tempDir1, tempDir2, historyFile, historyFile1, historyFile2, 
                   alreadyTransferedFile, historyDays, archiverTime, watcherEscalationTimeout, watcherSleepTime
            FROM BasicConfig
            WHERE id = ?
        """, (config_manager.config_id,))
        
        row = cursor.fetchone()
        conn.close()
        return row if row else None

    def save_fields_to_db(self):
        # Save data from input fields back to the database
        data = (
            self.stage_input.text(),
            self.temp_dir_input.text(),
            self.temp_dir1_input.text(),
            self.temp_dir2_input.text(),
            self.history_file_input.text(),
            self.history_file1_input.text(),
            self.history_file2_input.text(),
            "true" if self.already_transferred_file_input.isChecked() else "false",
            self.history_days_input.text(),
            self.archiver_time_input.text(),
            self.watcher_escalation_timeout_input.text(),
            self.watcher_sleep_time_input.text(),
            config_manager.config_id
        )

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE BasicConfig
            SET stage = ?, tempDir = ?, tempDir1 = ?, tempDir2 = ?, historyFile = ?, 
                historyFile1 = ?, historyFile2 = ?, alreadyTransferedFile = ?, historyDays = ?, 
                archiverTime = ?, watcherEscalationTimeout = ?, watcherSleepTime = ?
            WHERE id = ?
        """, data)
        
        conn.commit()
        conn.close()

        # Show success message
        self.popup_message.show_message("Changes in Basic Configuration have been successfully saved.")
