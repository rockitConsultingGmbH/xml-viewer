from PyQt5.QtWidgets import (QVBoxLayout, QFormLayout, QCheckBox,
                             QLineEdit, QWidget)
from common import config_manager
from controllers.connection_manager import ConnectionManager
from database.utils import select_from_mqconfig, update_mqconfig
from gui.popup_message_ui import PopupMessage
from gui.buttons import create_button_layout

class MQConfigurationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.conn_manager = ConnectionManager().get_instance()
        self.setup_ui()
        self.popup_message = PopupMessage(self)

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Initialize buttons and add them at the top
        button_layout = create_button_layout(self)
        layout.addLayout(button_layout)

        # Create and add the form layout
        form_layout = QFormLayout()
        self.init_input_fields()
        self.set_input_field_sizes()
        self.populate_fields_from_db()
        self.add_fields_to_form_layout(form_layout)
        
        layout.addLayout(form_layout)
        self.setLayout(layout)

    def init_input_fields(self):
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

    def set_input_field_sizes(self):
        input_fields = [
            self.qmgr_input, self.hostname_input, self.port_input, self.channel_input,
            self.userid_input, self.password_input, self.cipher_input, self.sslPeer_input,
            self.ccsid_input, self.queue_input, self.number_of_threads_input,
            self.error_queue_input, self.command_queue_input, self.command_reply_queue_input,
            self.wait_interval_input
        ]
        for field in input_fields:
            field.setFixedSize(500, 35)

    def add_fields_to_form_layout(self, form_layout):
        form_layout.addRow("Remote:", self.is_remote_input)
        form_layout.addRow("Queue manager:", self.qmgr_input)
        form_layout.addRow("Hostname:", self.hostname_input)
        form_layout.addRow("Port:", self.port_input)
        form_layout.addRow("Channel:", self.channel_input)
        form_layout.addRow("User Id:", self.userid_input)
        form_layout.addRow("Password:", self.password_input)
        form_layout.addRow("Cipher:", self.cipher_input)
        form_layout.addRow("SSL Peer:", self.sslPeer_input)
        form_layout.addRow("CCSID:", self.ccsid_input)
        form_layout.addRow("Queue:", self.queue_input)
        form_layout.addRow("Number of Threads:", self.number_of_threads_input)
        form_layout.addRow("Error Queue:", self.error_queue_input)
        form_layout.addRow("Command Queue:", self.command_queue_input)
        form_layout.addRow("Command Reply Queue:", self.command_reply_queue_input)
        form_layout.addRow("Wait Interval:", self.wait_interval_input)

    def populate_fields_from_db(self):
        data = self.get_mq_configuration()
        if data:
            self.is_remote_input.setChecked(data["isRemote"] == "true")
            self.qmgr_input.setText(data["qmgr"])
            self.hostname_input.setText(data["hostname"])
            self.port_input.setText(data["port"])
            self.channel_input.setText(data["channel"])
            self.userid_input.setText(data["userid"])
            self.password_input.setText(data["password"])
            self.cipher_input.setText(data["cipher"])
            self.sslPeer_input.setText(data["sslPeer"])
            self.ccsid_input.setText(data["ccsid"])
            self.queue_input.setText(data["queue"])
            self.number_of_threads_input.setText(data["numberOfThreads"])
            self.error_queue_input.setText(data["errorQueue"])
            self.command_queue_input.setText(data["commandQueue"])
            self.command_reply_queue_input.setText(data["commandReplyQueue"])
            self.wait_interval_input.setText(data["waitinterval"])

    def get_mq_configuration(self):
        conn = self.conn_manager.get_db_connection()
        cursor = conn.cursor()
        cursor = select_from_mqconfig(cursor, config_manager.config_id)
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def save_fields_to_db(self):
        mqconfig_data = {
            "isRemote": "true" if self.is_remote_input.isChecked() else "false",
            "qmgr": self.qmgr_input.text(),
            "hostname": self.hostname_input.text(),
            "port": self.port_input.text(),
            "channel": self.channel_input.text(),
            "userid": self.userid_input.text(),
            "password": self.password_input.text(),
            "cipher": self.cipher_input.text(),
            "sslPeer": self.sslPeer_input.text(),
            "ccsid": self.ccsid_input.text(),
            "queue": self.queue_input.text(),
            "numberOfThreads": self.number_of_threads_input.text(),
            "errorQueue": self.error_queue_input.text(),
            "commandQueue": self.command_queue_input.text(),
            "commandReplyQueue": self.command_reply_queue_input.text(),
            "waitinterval": self.wait_interval_input.text(),
            "description": '',
            "basicConfig_id": config_manager.config_id
        }

        conn = self.conn_manager.get_db_connection()
        cursor = conn.cursor()
        update_mqconfig(cursor, mqconfig_data)
        conn.commit()
        conn.close()
        
        # Show success message
        self.popup_message.show_message("Changes in MQ Configuration have been successfully saved.")
