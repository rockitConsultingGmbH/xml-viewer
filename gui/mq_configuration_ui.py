from PyQt5.QtWidgets import QVBoxLayout, QGroupBox, QHBoxLayout, QCheckBox, QPushButton, QLabel, \
    QLineEdit, QFormLayout, QSpacerItem, QSizePolicy, QScrollArea, QWidget, QFrame, QComboBox
from PyQt5.QtCore import Qt

from common import config_manager
from database.xml_data_to_db import get_db_connection
from gui.communication_ui import ClickableLabel, create_group, toggle_inputs

class MQConfigurationWidget(QWidget):
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
        self.is_remote_input = QLineEdit()
        self.qmgr_input = QLineEdit()
        self.hostname_input = QLineEdit()
        self.port_input = QLineEdit()
        self.channel_input = QLineEdit()
        self.userid_input = QLineEdit()
        self.password_input = QLineEdit()
        self.cipher_input = QLineEdit()
        self.sslPeer_input = QLineEdit()
        self.ccsid_input = QLineEdit()
        self.queue_input = QLineEdit()
        self.number_of_threads_input = QLineEdit()
        self.error_queue_input = QLineEdit()
        self.command_queue_input = QLineEdit()
        self.command_reply_queue_input = QLineEdit()
        self.wait_interval_input = QLineEdit()

        self.populate_fields_from_db()

        # Add each field to the form layout
        form_layout.addRow("Remote:", self.is_remote_input)
        form_layout.addRow("Queue manager:", self.qmgr_input)
        form_layout.addRow("Hostname:", self.hostname_input)
        form_layout.addRow("Port:", self.port_input)
        form_layout.addRow("Channel:", self.channel_input)
        form_layout.addRow("User Id::", self.userid_input)
        form_layout.addRow("User Password:", self.password_input)
        form_layout.addRow("Cipher:", self.cipher_input)
        form_layout.addRow("SSL Peer:", self.sslPeer_input)
        form_layout.addRow("CCSID:", self.ccsid_input)
        form_layout.addRow("Queue Name:", self.queue_input)
        form_layout.addRow("Number Of Threads:", self.number_of_threads_input)
        form_layout.addRow("Error Queue:", self.error_queue_input)
        form_layout.addRow("Command Queue:", self.command_queue_input)
        form_layout.addRow("Command Reply Queue:", self.command_reply_queue_input)
        form_layout.addRow("Wait Interval:", self.wait_interval_input)

        # Set form layout to the main layout
        layout.addLayout(form_layout)

    def populate_fields_from_db(self):
        # Call the function to fetch data from the database
        data = self.get_mq_configuration()
        print(data)
        # Ensure data is available
        if data:
            # Populate the fields
            self.is_remote_input.setText(data[0])
            self.qmgr_input.setText(data[1])
            self.hostname_input.setText(data[2])
            self.port_input.setText(data[3])
            self.channel_input.setText(data[4])
            self.userid_input.setText(data[5])
            self.password_input.setText(data[6])
            self.cipher_input.setText(data[7])
            self.sslPeer_input.setText(data[8])
            self.ccsid_input.setText(data[9])
            self.queue_input.setText(data[10])
            self.number_of_threads_input.setText(data[11])
            self.error_queue_input.setText(data[12])
            self.command_queue_input.setText(data[13])
            self.command_reply_queue_input.setText(data[14])
            self.wait_interval_input.setText(data[15])

    def get_mq_configuration(self):
        conn = get_db_connection()  # Assuming this function is defined elsewhere
        cursor = conn.cursor()
        
        # Replace with the actual query you need for your configuration
        cursor.execute(f"SELECT isRemote, qmgr, hostname, port, channel, userid, \
                       password, cipher, sslPeer, ccsid, queue, numberOfThreads, errorQueue, commandQueue, commandReplyQueue, waitinterval FROM MqConfig WHERE basicConfig_id = {config_manager.config_id}")
        row = cursor.fetchone()
        
        # Close the database connection
        conn.close()
        
        # Ensure a row was retrieved and return it
        if row:
            return row
        else:
            return None