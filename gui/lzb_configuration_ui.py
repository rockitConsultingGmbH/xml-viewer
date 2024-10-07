from PyQt5.QtWidgets import QVBoxLayout, QGroupBox, QHBoxLayout, QCheckBox, QPushButton, QLabel, \
    QLineEdit, QFormLayout, QSpacerItem, QSizePolicy, QScrollArea, QWidget, QFrame, QComboBox
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
        #reset_button.clicked.connect(self.reset_fields)  # Connect to reset function

        save_button = QPushButton("Save")
        save_button.setFixedSize(100, 30)
        save_button.setStyleSheet("background-color: #41414a; color: white;")
        #save_button.clicked.connect(self.save_fields_to_db)  # Connect to save function

        button_layout.addWidget(reset_button)
        button_layout.addWidget(save_button)

        # Add button layout to form layout
        form_layout.addRow(button_layout)

        # Define the input fields
        self.encrypt_key_input = QLineEdit() 
        self.encrypt_enabled_input = QLineEdit()
        self.keystore_path_input = QLineEdit()
        self.keystore_password_input = QLineEdit()
        self.truststore_path_input = QLineEdit()
        self.truststore_password_input = QLineEdit()
        self.ssh_implementation_input = QLineEdit()
        self.dns_timeout_input = QLineEdit()

        self.populate_fields_from_db()

        # Add each field to the form layout
        form_layout.addRow("Encrypt_Key:", self.encrypt_key_input)
        form_layout.addRow("Encrypt:", self.encrypt_enabled_input)
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
            self.encrypt_enabled_input.setText(str(data[1]))
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