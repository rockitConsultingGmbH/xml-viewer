from PyQt5.QtWidgets import QVBoxLayout, QCheckBox, QLineEdit, QFormLayout, QWidget, QGroupBox
from PyQt5.QtGui import QFont
from common import config_manager
from common.connection_manager import ConnectionManager
from database.utils import select_from_lzbconfig, update_lzbconfig
from gui.components.popup_message_ui import PopupMessage
from gui.components.buttons import ButtonFactory

class LZBConfigurationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.conn_manager = ConnectionManager().get_instance()
        self.popup_message = PopupMessage(self)
        self.setup_ui()
    
    def setup_ui(self):
        # Set up the main layout and form layout
        lzb_config_group = QGroupBox("LZB Configuration")
        lzb_config_group.setFont(QFont("Arial", 10, QFont.Bold))
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        # Set up Save and Reset buttons
        button_layout = ButtonFactory().create_button_layout(self)

        # Initialize input fields
        self.initialize_fields()
        
        # Add input fields to the form layout
        self.add_fields_to_layout(form_layout)

        # Set the layout for the widget
        lzb_config_group.setLayout(form_layout)
        layout.addLayout(button_layout)
        layout.addWidget(lzb_config_group)

        # Populate fields with data from the database
        self.set_fields_from_db()

    def initialize_fields(self):
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
        self.dns_timeout_input.setFixedSize(500, 35)

    def apply_field_size(self, *fields):
        for field in fields:
            field.setFixedSize(500, 35)

    def add_fields_to_layout(self, layout):
        layout.addRow("Encrypt:", self.encrypt_enabled_input)
        layout.addRow("Encrypt Key:", self.encrypt_key_input)
        layout.addRow("Keystore Path:", self.keystore_path_input)
        layout.addRow("Keystore Password:", self.keystore_password_input)
        layout.addRow("Truststore Path:", self.truststore_path_input)
        layout.addRow("Truststore Password:", self.truststore_password_input)
        layout.addRow("SSH Implementation:", self.ssh_implementation_input)
        layout.addRow("DNS Timeout:", self.dns_timeout_input)

    def set_fields_from_db(self):
        data = self.get_lzb_configuration()
        if data:
            self.encrypt_key_input.setText(data["encrypt_key"])
            self.encrypt_enabled_input.setChecked(data["encrypt_enabled"] == "true")
            self.keystore_path_input.setText(data["keystore_path"])
            self.keystore_password_input.setText(data["keystore_password"])
            self.truststore_path_input.setText(data["truststore_path"])
            self.truststore_password_input.setText(data["truststore_password"])
            self.ssh_implementation_input.setText(data["ssh_implementation"])
            self.dns_timeout_input.setText(str(data["dns_timeout"]))

    def get_lzb_configuration(self):
        conn = self.conn_manager.get_db_connection()
        cursor = conn.cursor()
        select_from_lzbconfig(cursor, config_manager.config_id )
        row = cursor.fetchone()
        conn.close()
        
        return row if row else None

    def save_fields_to_db(self):
        # Save data from input fields back to the database       
        row = {
            'encrypt_key': self.encrypt_key_input.text(),
            'encrypt_enabled': "true" if self.encrypt_enabled_input.isChecked() else "false",
            'keystore_path': self.keystore_path_input.text(),
            'keystore_password': self.keystore_password_input.text(),
            'truststore_path': self.truststore_path_input.text(),
            'truststore_password': self.truststore_password_input.text(),
            'ssh_implementation': self.ssh_implementation_input.text(),
            'dns_timeout': self.dns_timeout_input.text(), 
            'basicConfig_id': config_manager.config_id
        }

        conn = self.conn_manager.get_db_connection()
        cursor = conn.cursor()
        update_lzbconfig(cursor, row)
        conn.commit()
        conn.close()

        # Show success message
        self.popup_message.show_message("Changes have been successfully saved.")
