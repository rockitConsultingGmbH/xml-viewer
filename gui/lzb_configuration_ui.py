from PyQt5.QtWidgets import QVBoxLayout, QCheckBox, QPushButton, QLineEdit, QFormLayout, QWidget
from common import config_manager
from database.connection_manager import ConnectionManager
from database.xml_to_db import get_db_connection
from gui.popup_message_ui import PopupMessage
from gui.buttons import create_button_layout

# Define constants for button and field styling
BUTTON_STYLE = "background-color: {}; color: white;"
FIELD_SIZE = (500, 35)
BUTTON_SIZE = (100, 30)

class LZBConfigurationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.conn_manager = ConnectionManager()
        self.popup_message = PopupMessage(self)
        self.setup_ui()
    
    def setup_ui(self):
        # Set up the main layout and form layout
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        # Set up Save and Reset buttons
        button_layout = create_button_layout(self)
        form_layout.addRow(button_layout)

        # Initialize input fields
        self.initialize_fields()
        
        # Add input fields to the form layout
        self.add_fields_to_layout(form_layout)

        # Set the layout for the widget
        layout.addLayout(form_layout)

        # Populate fields with data from the database
        self.populate_fields_from_db()

    def initialize_fields(self):
        """Initialize input fields with specific properties."""
        self.encrypt_key_input = QLineEdit()
        self.encrypt_enabled_input = QCheckBox()
        self.keystore_path_input = QLineEdit()
        self.keystore_password_input = QLineEdit()
        self.truststore_path_input = QLineEdit()
        self.truststore_password_input = QLineEdit()
        self.ssh_implementation_input = QLineEdit()
        self.dns_timeout_input = QLineEdit()

        # Apply a fixed size to fields where appropriate
        self.apply_field_size(self.encrypt_key_input, self.keystore_path_input, 
                              self.keystore_password_input, self.truststore_path_input, 
                              self.truststore_password_input, self.ssh_implementation_input)
        self.dns_timeout_input.setFixedSize(100, 35)  # Custom width for dns_timeout

    def apply_field_size(self, *fields):
        """Applies a fixed size to multiple input fields."""
        for field in fields:
            field.setFixedSize(*FIELD_SIZE)

    def add_fields_to_layout(self, layout):
        """Add input fields to the form layout with appropriate labels."""
        layout.addRow("Encrypt:", self.encrypt_enabled_input)
        layout.addRow("Encrypt Key:", self.encrypt_key_input)
        layout.addRow("Keystore Path:", self.keystore_path_input)
        layout.addRow("Keystore Password:", self.keystore_password_input)
        layout.addRow("Truststore Path:", self.truststore_path_input)
        layout.addRow("Truststore Password:", self.truststore_password_input)
        layout.addRow("SSH Implementation:", self.ssh_implementation_input)
        layout.addRow("DNS Timeout:", self.dns_timeout_input)

    def populate_fields_from_db(self):
        """Fetches and populates the widget fields with data from the database."""
        data = self.get_lzb_configuration()
        if data:
            self.encrypt_key_input.setText(data[0])
            self.encrypt_enabled_input.setChecked(data[1] == "true")
            self.keystore_path_input.setText(data[2])
            self.keystore_password_input.setText(data[3])
            self.truststore_path_input.setText(data[4])
            self.truststore_password_input.setText(data[5])
            self.ssh_implementation_input.setText(data[6])
            self.dns_timeout_input.setText(str(data[7]))

    def get_lzb_configuration(self):
        """Retrieve LZB configuration from the database."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT encrypt_key, encrypt_enabled, keystore_path, keystore_password, 
                   truststore_path, truststore_password, ssh_implementation, dns_timeout 
            FROM LzbConfig 
            WHERE basicConfig_id = ?
        """
        cursor.execute(query, (config_manager.config_id,))
        row = cursor.fetchone()
        conn.close()
        
        return row if row else None

    def save_fields_to_db(self):
        """Saves the current state of the fields to the database."""
        values = (
            self.encrypt_key_input.text(),
            "true" if self.encrypt_enabled_input.isChecked() else "false",
            self.keystore_path_input.text(),
            self.keystore_password_input.text(),
            self.truststore_path_input.text(),
            self.truststore_password_input.text(),
            self.ssh_implementation_input.text(),
            self.dns_timeout_input.text(), 
            config_manager.config_id
        )

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            UPDATE LzbConfig
            SET encrypt_key = ?, encrypt_enabled = ?, keystore_path = ?, keystore_password = ?, 
                truststore_path = ?, truststore_password = ?, ssh_implementation = ?, dns_timeout = ?
            WHERE basicConfig_id = ?
        """
        cursor.execute(query, values)
        conn.commit()
        conn.close()

        # Show success message
        self.popup_message.show_message("Changes in LZB Configuration have been successfully saved.")
