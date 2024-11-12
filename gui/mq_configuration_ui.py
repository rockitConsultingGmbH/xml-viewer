from PyQt5.QtWidgets import (QVBoxLayout, QFormLayout, QCheckBox, QLineEdit, QWidget, QScrollArea, QGroupBox, QSpacerItem, QSizePolicy, QFrame)
from PyQt5.QtGui import QFont
from common.config_manager import ConfigManager
from common.connection_manager import ConnectionManager
from database.utils import select_from_ipqueue, select_from_mqconfig, select_from_mqtrigger, update_ipqueue, update_mqconfig, update_mqtrigger
from gui.common_components.popup_message import PopupMessage
from gui.common_components.buttons import Buttons
from gui.common_components.stylesheet_loader import load_stylesheet
from gui.mq_configuration_components.ipqueue_configuration import IPQueueConfiguration
from gui.mq_configuration_components.mqtrigger_configuration import MQTriggerConfiguration


class MQConfigurationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.conn_manager = ConnectionManager()
        self.config_manager = ConfigManager()
        self.popup_message = PopupMessage(self)
        self.mqtrigger_configuration = MQTriggerConfiguration()
        self.ipqueue_configuration = IPQueueConfiguration()
        self.ipqueue_fields = []
        self.setup_ui()

        load_stylesheet(self, "css/right_widget_styling.qss")

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        button_layout = Buttons().create_button_layout(self)
        main_layout.addLayout(button_layout)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.NoFrame)

        scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_content)

        self.create_mqconfig_layout(self.scroll_layout)
        self.add_groupbox_spacing(self.scroll_layout)
        self.mqtrigger_configuration.create_mqtrigger_layout(self.scroll_layout)
        self.add_groupbox_spacing(self.scroll_layout)
        self.ipqueue_configuration.create_ipqueue_layout(self.scroll_layout)

        self.scroll_area.setWidget(scroll_content)
        main_layout.addWidget(self.scroll_area)
        self.setLayout(main_layout)

    def add_groupbox_spacing(self, layout):
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        layout.addItem(spacer)

    def create_mqconfig_layout(self, parent_layout):
        mqconfig_group = QGroupBox("MQ Configuration")
        mqconfig_group.setObjectName("group-border")
        mqconfig_group.setFont(QFont("Arial", 12, QFont.Bold))
        mqconfig_group.setStyleSheet("QLabel { border: none; font-size: 12px; } QLineEdit, QCheckBox { font-size: 12px; }")
        mqconfig_layout = QFormLayout()

        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        mqconfig_layout.addItem(spacer)

        self.add_mqconfig_fields_to_form_layout(mqconfig_layout)
        self.populate_mqconfig_fields_from_db()
        mqconfig_group.setLayout(mqconfig_layout)
        parent_layout.addWidget(mqconfig_group)

    def add_mqconfig_fields_to_form_layout(self, form_layout):
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

        fields = [
            (self.qmgr_input, "Queue Manager:"),
            (self.hostname_input, "Hostname:"),
            (self.port_input, "Port:"),
            (self.channel_input, "Channel:"),
            (self.userid_input, "User ID:"),
            (self.password_input, "Password:"),
            (self.cipher_input, "Cipher:"),
            (self.sslPeer_input, "SSL Peer:"),
            (self.ccsid_input, "CCSID:"),
            (self.queue_input, "Queue:"),
            (self.number_of_threads_input, "Number of Threads:"),
            (self.error_queue_input, "Error Queue:"),
            (self.command_queue_input, "Command Queue:"),
            (self.command_reply_queue_input, "Command Reply Queue:"),
            (self.wait_interval_input, "Wait Interval:")
        ]

        for field, label in fields:
            field.setFixedWidth(500)
            field.setFixedHeight(35)
            form_layout.addRow(label, field)

        form_layout.addRow("Remote:", self.is_remote_input)

    def populate_mqconfig_fields_from_db(self):
        data = self.get_mqconfig_data()
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

    def get_mqconfig_data(self):
        conn = self.conn_manager.get_db_connection()
        cursor = conn.cursor()
        cursor = select_from_mqconfig(cursor, self.config_manager.config_id)
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def save_mqconfig_fields_to_db(self, cursor):
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
            "basicConfig_id": self.config_manager.config_id
        }

        update_mqconfig(cursor, mqconfig_data)
        return cursor

    def save_fields_to_db(self):
        try:
            conn = self.conn_manager.get_db_connection()
            cursor = conn.cursor()
            self.save_mqconfig_fields_to_db(cursor)
            self.mqtrigger_configuration.save_mqtrigger_fields_to_db(cursor)
            self.ipqueue_configuration.save_ipqueue_fields_to_db(cursor)
            conn.commit()
            self.popup_message.show_message("Changes have been successfully saved.")
        except Exception as e:
            print(f"Error while saving data: {e}")
            conn.rollback()
            self.popup_message.show_error_message(f"Error while saving data: {e}")
        finally:
            conn.close()

    def set_fields_from_db(self):
        try:
            self.populate_mqconfig_fields_from_db()
            self.mqtrigger_configuration.populate_mqtrigger_fields_from_db()
            self.ipqueue_configuration.populate_ipqueue_fields_from_db()
        except Exception as e:
            print(f"Error populating fields from database: {e}")
            self.popup_message.show_error_message("Error populating fields from database.")

    def refresh_page(self):
        self.clear_layout(self.scroll_layout)
        self.create_mqconfig_layout(self.scroll_layout)
        self.add_groupbox_spacing(self.scroll_layout)
        self.mqtrigger_configuration.create_mqtrigger_layout(self.scroll_layout)
        self.add_groupbox_spacing(self.scroll_layout)
        self.ipqueue_configuration.create_ipqueue_layout(self.scroll_layout)
        self.repaint()

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
