from PyQt5.QtWidgets import QVBoxLayout, QGroupBox, QHBoxLayout, QCheckBox, QPushButton, QLabel, \
    QLineEdit, QFormLayout, QSpacerItem, QSizePolicy, QScrollArea, QWidget, QFrame, QComboBox, QMessageBox
from PyQt5.QtCore import Qt, QTimer

from common import config_manager
from database.xml_to_db import get_db_connection
from gui.communication_ui import ClickableLabel, create_group, toggle_inputs

class MQConfigurationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        # Create the layout and form layout
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

         # Create the success message label
        self.success_message = QLabel()
        self.success_message.setStyleSheet("background-color: lightgreen; color: black; padding: 5px;")
        self.success_message.setAlignment(Qt.AlignCenter)
        self.success_message.setFixedHeight(30)
        self.success_message.setVisible(False)

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
        form_layout.addRow(self.success_message)
        form_layout.addRow(button_layout)

        # Define the input fields
        self.is_remote_input = QCheckBox()
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

        self.qmgr_input.setFixedSize(500, 35)
        self.hostname_input.setFixedSize(500, 35)
        self.port_input.setFixedSize(500, 35)
        self.channel_input.setFixedSize(500, 35)
        self.userid_input.setFixedSize(500, 35)
        self.password_input.setFixedSize(500, 35)
        self.cipher_input.setFixedSize(500, 35)
        self.sslPeer_input.setFixedSize(500, 35)
        self.ccsid_input.setFixedSize(500, 35)
        self.queue_input.setFixedSize(500, 35)
        self.number_of_threads_input.setFixedSize(500, 35)
        self.error_queue_input.setFixedSize(500, 35)
        self.command_queue_input.setFixedSize(500, 35)
        self.command_reply_queue_input.setFixedSize(500, 35)
        self.wait_interval_input.setFixedSize(500, 35)

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

        self.setLayout(layout)
        # Initialize the timer for the success message
        self.message_timer = QTimer()
        self.message_timer.setSingleShot(True)
        self.message_timer.timeout.connect(self.hide_success_message)

    def populate_fields_from_db(self):
        # Call the function to fetch data from the database
        data = self.get_mq_configuration()
        print(data)
        # Ensure data is available
        if data:
            # Populate the fields
            #self.is_remote_input.setText(data[0])
            self.is_remote_input.setChecked(True) if data[0] == "true" else self.is_remote_input.setChecked(False)
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

    def save_fields_to_db(self):
        # Get the values from the input fields
        is_remote = "true" if self.is_remote_input.isChecked() else "false"
        qmgr = self.qmgr_input.text()
        hostname = self.hostname_input.text()
        port = self.port_input.text()
        channel = self.channel_input.text()
        userid = self.userid_input.text()
        password = self.password_input.text()
        cipher = self.cipher_input.text()
        sslPeer = self.sslPeer_input.text()
        ccsid = self.ccsid_input.text()
        queue = self.queue_input.text()
        number_of_threads = self.number_of_threads_input.text()
        error_queue = self.error_queue_input.text()
        command_queue = self.command_queue_input.text()
        command_reply_queue = self.command_reply_queue_input.text()
        wait_interval = self.wait_interval_input.text()

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Execute the update query
        cursor.execute("""
            UPDATE MqConfig 
            SET isRemote = ?, qmgr = ?, hostname = ?, port = ?, channel = ?, userid = ?, 
                password = ?, cipher = ?, sslPeer = ?, ccsid = ?, queue = ?, numberOfThreads = ?, 
                errorQueue = ?, commandQueue = ?, commandReplyQueue = ?, waitinterval = ?
            WHERE basicConfig_id = ?
        """, (is_remote, qmgr, hostname, port, channel, userid, password, cipher, sslPeer,
            ccsid, queue, number_of_threads, error_queue, command_queue, command_reply_queue, 
            wait_interval, config_manager.config_id))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        # Optionally, show a message box or print a message to confirm saving
        print("Configuration updated successfully.")
        self.show_success_message("Changes in MQ Configuration have been successfully saved.")

        # Show success message
        #msg = QMessageBox()
        #msg.setIcon(QMessageBox.Information)
        #msg.setText("Changes in MQ Configuration have been successfully saved.")
        #msg.setWindowTitle("Save Successful")
        #msg.setStandardButtons(QMessageBox.Ok)
        #msg.exec_()

    def show_success_message(self, text):
        # Set the message text and show the label
        self.success_message.setText(text)
        self.success_message.setVisible(True)
        self.message_timer.start(3000)  # Show message for 3 seconds
											  
    def hide_success_message(self):
        self.success_message.setVisible(False)
