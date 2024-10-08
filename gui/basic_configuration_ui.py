from PyQt5.QtWidgets import QVBoxLayout, QGroupBox, QHBoxLayout, QCheckBox, QPushButton, QLabel, \
    QLineEdit, QFormLayout, QSpacerItem, QSizePolicy, QScrollArea, QWidget, QFrame, QComboBox, QMessageBox
from PyQt5.QtCore import Qt

from common import config_manager
from database.xml_data_to_db import get_db_connection
from gui.communication_ui import ClickableLabel, create_group, toggle_inputs

class BasicConfigurationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        # Create the layout and form layout
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        # Create Save and Reset buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        reset_button = QPushButton("Reset")
        reset_button.setFixedSize(100, 30)
        reset_button.setStyleSheet("background-color: #960e0e; color: white;")
        reset_button.clicked.connect(self.populate_fields_from_db)  # Connect to reset function

        save_button = QPushButton("Save")
        save_button.setFixedSize(100, 30)
        save_button.setStyleSheet("background-color: #41414a; color: white;")
        save_button.clicked.connect(self.save_fields_to_db)

        button_layout.addWidget(reset_button)
        button_layout.addWidget(save_button)

        # Add button layout to form layout
        form_layout.addRow(button_layout)

        # Define the input fields
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

        self.stage_input.setFixedSize(100, 35)
        self.temp_dir_input.setFixedSize(500, 35)
        self.temp_dir1_input.setFixedSize(500, 35)
        self.temp_dir2_input.setFixedSize(500, 35)
        self.history_file_input.setFixedSize(500, 35)
        self.history_file1_input.setFixedSize(500, 35)
        self.history_file2_input.setFixedSize(500, 35)
        #self.already_transferred_file_input.setFixedSize(500, 35)
        self.history_days_input.setFixedSize(100, 35)
        self.archiver_time_input.setFixedSize(100, 35)
        self.watcher_escalation_timeout_input.setFixedSize(100, 35)
        self.watcher_sleep_time_input.setFixedSize(100, 35)

        self.populate_fields_from_db()

        # Add each field to the form layout
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

        # Set form layout to the main layout
        layout.addLayout(form_layout)

    def populate_fields_from_db(self):
        # Call the function to fetch data from the database
        data = self.get_basic_configuration()
        print(data)
        # Ensure data is available
        if data:
            # Populate the fields
            self.stage_input.setText(data[0])
            self.temp_dir_input.setText(data[1])
            self.temp_dir1_input.setText(data[2])
            self.temp_dir2_input.setText(data[3])
            self.history_file_input.setText(data[4])
            self.history_file1_input.setText(data[5])
            self.history_file2_input.setText(data[6])
            #self.already_transferred_file_input.setText(data[7])
            self.already_transferred_file_input.setChecked(True) if data[7] == "1" else self.already_transferred_file_input.setChecked(False) #TODO: Type in DB should be changed to int
            self.history_days_input.setText(data[8])
            self.archiver_time_input.setText(data[9])
            self.watcher_escalation_timeout_input.setText(data[10])
            self.watcher_sleep_time_input.setText(data[11])

    def get_basic_configuration(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Replace with the actual query you need for your configuration
        cursor.execute(f"SELECT stage, tempDir, tempDir1, tempDir2, historyFile, historyFile1, historyFile2, alreadyTransferedFile, historyDays,\
        archiverTime, watcherEscalationTimeout, watcherSleepTime FROM BasicConfig WHERE id = {config_manager.config_id}")
        row = cursor.fetchone()
        
        # Close the database connection
        conn.close()
        
        # Ensure a row was retrieved and return it
        if row:
            return row
        else:
            return None

    def save_fields_to_db(self):
        # Gather data from input fields
        stage = self.stage_input.text()
        temp_dir = self.temp_dir_input.text()
        temp_dir1 = self.temp_dir1_input.text()
        temp_dir2 = self.temp_dir2_input.text()
        history_file = self.history_file_input.text()
        history_file1 = self.history_file1_input.text()
        history_file2 = self.history_file2_input.text()
        already_transferred_file = 1 if self.already_transferred_file_input.isChecked() else 0
        history_days = self.history_days_input.text() #int(self.history_days_input.text()) if self.history_days_input.text().isdigit() else 0
        archiver_time = self.archiver_time_input.text()
        watcher_escalation_timeout = self.watcher_escalation_timeout_input.text() #int(self.watcher_escalation_timeout_input.text()) if self.watcher_escalation_timeout_input.text().isdigit() else 0
        watcher_sleep_time = self.watcher_sleep_time_input.text()

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Execute the update query
        cursor.execute("""
            UPDATE BasicConfig
            SET stage = ?, tempDir = ?, tempDir1 = ?, tempDir2 = ?, historyFile = ?, 
                historyFile1 = ?, historyFile2 = ?, alreadyTransferedFile = ?, historyDays = ?, 
                archiverTime = ?, watcherEscalationTimeout = ?, watcherSleepTime = ?
            WHERE id = ?
        """, (stage, temp_dir, temp_dir1, temp_dir2, history_file, history_file1, history_file2, 
            already_transferred_file, history_days, archiver_time, watcher_escalation_timeout, 
            watcher_sleep_time, config_manager.config_id))

        # Commit and close the connection
        conn.commit()
        conn.close()

        # Optionally, print a confirmation message
        print("Basic configuration updated successfully.")

        # Show success message
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Changes in Basic Configuration have been successfully saved.")
        msg.setWindowTitle("Save Successful")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
