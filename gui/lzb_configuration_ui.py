from PyQt5.QtWidgets import QVBoxLayout, QGroupBox, QHBoxLayout, QCheckBox, QPushButton, QLabel, \
    QLineEdit, QFormLayout, QSpacerItem, QSizePolicy, QScrollArea, QWidget, QFrame, QComboBox, QMessageBox
from PyQt5.QtCore import Qt

from common import config_manager
from database.xml_data_to_db import get_db_connection
from gui.communication_ui import ClickableLabel, create_group, toggle_inputs

class LZBConfigurationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        # Create Save and Reset buttons
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

        # Add button layout to form layout
        form_layout.addRow(button_layout)

        # Define the input fields
        self.encrypt_key_input = QLineEdit()
        self.encrypt_enabled_input = QCheckBox()
        self.keystore_path_input = QLineEdit()
        self.keystore_password_input = QLineEdit()
        self.truststore_path_input = QLineEdit()
        self.truststore_password_input = QLineEdit()
        self.ssh_implementation_input = QLineEdit()
        self.dns_timeout_input = QLineEdit()

        self.encrypt_key_input.setFixedSize(500, 35)
        #self.encrypt_enabled_input.setFixedSize(500, 35)
        self.keystore_path_input.setFixedSize(500, 35)
        self.keystore_password_input.setFixedSize(500, 35)
        self.truststore_path_input.setFixedSize(500, 35)
        self.truststore_password_input.setFixedSize(500, 35)
        self.ssh_implementation_input.setFixedSize(500, 35)
        self.dns_timeout_input.setFixedSize(100, 35)
        self.populate_fields_from_db()

        # Add each field to the form layout
        form_layout.addRow("Encrypt:", self.encrypt_enabled_input)
        form_layout.addRow("Encrypt_Key:", self.encrypt_key_input)
        form_layout.addRow("Keystore Path:", self.keystore_path_input)
        form_layout.addRow("Keystore_Password:", self.keystore_password_input)
        form_layout.addRow("Truststore Path:", self.truststore_path_input)
        form_layout.addRow("Truststore Password:", self.truststore_password_input)
        form_layout.addRow("SSH Implementation:", self.ssh_implementation_input)
        form_layout.addRow("DNS Timeout:", self.dns_timeout_input)

        # Set form layout to the main layout
        layout.addLayout(form_layout)

    def populate_fields_from_db(self):
        # Call the function to fetch data from the database
        data = self.get_lzb_configuration()
        print(data)
        # Ensure data is available
        if data:
            # Populate the fields
            self.encrypt_key_input.setText(data[0])
            #self.encrypt_enabled_input.setText(str(data[1]))
            self.encrypt_enabled_input.setChecked(True) if data[1] == 1 else self.encrypt_enabled_input.setChecked(False)
            self.keystore_path_input.setText(data[2])
            self.keystore_password_input.setText(data[3])
            self.truststore_path_input.setText(data[4])
            self.truststore_password_input.setText(data[5])
            self.ssh_implementation_input.setText(data[6])
            self.dns_timeout_input.setText(str(data[7]))

    def get_lzb_configuration(self):
        conn = get_db_connection()  # Assuming this function is defined elsewhere
        cursor = conn.cursor()
        
        # Replace with the actual query you need for your configuration
        cursor.execute(f"SELECT encrypt_key, encrypt_enabled, keystore_path, keystore_password, \
                    truststore_path, truststore_password, ssh_implementation, dns_timeout FROM LzbConfig WHERE basicConfig_id = {config_manager.config_id}")
        row = cursor.fetchone()
        
        # Close the database connection
        conn.close()
        
        # Ensure a row was retrieved and return it
        if row:
            return row
        else:
            return None
        
    def save_fields_to_db(self):
        # Get the values from the input fields
        encrypt_key = self.encrypt_key_input.text()
        encrypt_enabled = 1 if self.encrypt_enabled_input.isChecked() else 0
        keystore_path = self.keystore_path_input.text()
        keystore_password = self.keystore_password_input.text()
        truststore_path = self.truststore_path_input.text()
        truststore_password = self.truststore_password_input.text()
        ssh_implementation = self.ssh_implementation_input.text()
        dns_timeout = self.dns_timeout_input.text() #int(self.dns_timeout_input.text()) if self.dns_timeout_input.text().isdigit() else 0

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Execute the update query
        cursor.execute("""
            UPDATE LzbConfig
            SET encrypt_key = ?, encrypt_enabled = ?, keystore_path = ?, keystore_password = ?, 
                truststore_path = ?, truststore_password = ?, ssh_implementation = ?, dns_timeout = ?
            WHERE basicConfig_id = ?
        """, (encrypt_key, encrypt_enabled, keystore_path, keystore_password, truststore_path, 
            truststore_password, ssh_implementation, dns_timeout, config_manager.config_id))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        # Optionally, show a message box or print a message to confirm saving
        print("LZB configuration updated successfully.")

        # Show success message
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Changes in LZB Configuration have been successfully saved.")
        msg.setWindowTitle("Save Successful")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()