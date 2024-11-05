from PyQt5.QtWidgets import (QVBoxLayout, QFormLayout, QCheckBox, QLineEdit, QWidget, QScrollArea, QGroupBox, QSpacerItem, QSizePolicy, QFrame)
from PyQt5.QtGui import QFont
from common.config_manager import ConfigManager
from common.connection_manager import ConnectionManager
from database.utils import select_from_ipqueue, select_from_mqconfig, select_from_mqtrigger, update_ipqueue, update_mqconfig, update_mqtrigger
from gui.common_components.popup_message import PopupMessage
from gui.common_components.buttons import Buttons
from gui.common_components.stylesheet_loader import load_stylesheet


class MQConfigurationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.conn_manager = ConnectionManager().get_instance()
        self.config_manager = ConfigManager()
        self.popup_message = PopupMessage(self)
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
        self.create_mqtrigger_layout(self.scroll_layout)
        self.add_groupbox_spacing(self.scroll_layout)
        self.create_ipqueue_layout(self.scroll_layout)

        self.scroll_area.setWidget(scroll_content)
        main_layout.addWidget(self.scroll_area)
        self.setLayout(main_layout)

    def add_groupbox_spacing(self, layout):
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed)
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

    def create_mqtrigger_layout(self, parent_layout):
        mqtrigger_group = QGroupBox("MQTrigger Settings")
        mqtrigger_group.setObjectName("group-border")
        mqtrigger_group.setFont(QFont("Arial", 12, QFont.Bold))
        mqtrigger_group.setStyleSheet("QLabel { border: none; font-size: 12px; } QLineEdit, QCheckBox { font-size: 12px; }")
        mqtrigger_layout = QFormLayout()

        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        mqtrigger_layout.addItem(spacer)

        self.add_mqtrigger_fields_to_form_layout(mqtrigger_layout)
        self.populate_mqtrigger_fields_from_db()

        mqtrigger_group.setLayout(mqtrigger_layout)
        parent_layout.addWidget(mqtrigger_group)

    def add_mqtrigger_fields_to_form_layout(self, form_layout):
        self.success_interval_input = QLineEdit()
        self.trigger_interval_input = QLineEdit()
        self.polling_input = QLineEdit()
        self.dynamic_instance_management_input = QLineEdit()
        self.dynamic_success_count_input = QLineEdit()
        self.dynamic_success_interval_input = QLineEdit()
        self.dynamic_max_instances_input = QLineEdit()

        fields = [
            (self.success_interval_input, "Success Interval:"),
            (self.trigger_interval_input, "Trigger Interval:"),
            (self.polling_input, "Polling:"),
            (self.dynamic_instance_management_input, "Dynamic Instance Management:"),
            (self.dynamic_success_count_input, "Dynamic Success Count:"),
            (self.dynamic_success_interval_input, "Dynamic Success Interval:"),
            (self.dynamic_max_instances_input, "Dynamic Max Instances:")
        ]

        for field, label in fields:
            field.setFixedWidth(500)
            field.setFixedHeight(35)
            form_layout.addRow(label, field)

    def populate_mqtrigger_fields_from_db(self):
        data = self.get_mqtrigger_data()
        if data:
            self.success_interval_input.setText(data["success_interval"])
            self.trigger_interval_input.setText(data["trigger_interval"])
            self.polling_input.setText(data["polling"])
            self.dynamic_instance_management_input.setText(data["dynamic_instance_management"])
            self.dynamic_success_count_input.setText(data["dynamic_success_count"])
            self.dynamic_success_interval_input.setText(data["dynamic_success_interval"])
            self.dynamic_max_instances_input.setText(data["dynamic_max_instances"])

    def get_mqtrigger_data(self):
        conn = self.conn_manager.get_db_connection()
        cursor = conn.cursor()
        cursor = select_from_mqtrigger(cursor, self.config_manager.config_id)
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def create_ipqueue_layout(self, parent_layout):
        ipqueue_group = QGroupBox("IPQueue Settings")
        ipqueue_group.setObjectName("group-border")
        ipqueue_group.setFont(QFont("Arial", 12, QFont.Bold))
        ipqueue_group.setStyleSheet("QLabel { border: none; font-size: 12px; } QLineEdit, QCheckBox { font-size: 12px; }")
        ipqueue_main_layout = QVBoxLayout()

        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        ipqueue_main_layout.addItem(spacer)

        ipqueue_entries = self.get_ipqueue_data()

        for entry in ipqueue_entries:
            individual_ipqueue_group = QGroupBox(f"IPQueue")
            individual_ipqueue_group.setObjectName("group-border")
            individual_ipqueue_group.setFont(QFont("Arial", 10, QFont.Bold, italic=True))
            individual_ipqueue_layout = QFormLayout()

            spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)
            individual_ipqueue_layout.addItem(spacer)

            individual_ipqueue_layout = self.add_ipqueue_fields_to_form_layout(individual_ipqueue_layout, entry)
            self.populate_ipqueue_fields_from_db()

            individual_ipqueue_group.setLayout(individual_ipqueue_layout)
            ipqueue_main_layout.addWidget(individual_ipqueue_group)
            ipqueue_main_layout.addSpacing(20)

        ipqueue_group.setLayout(ipqueue_main_layout)
        parent_layout.addWidget(ipqueue_group)

    def add_ipqueue_fields_to_form_layout(self, entry_layout, entry):
        ipqueue_input = QLineEdit()
        ipqueue_errorqueue_input = QLineEdit()
        ipqueue_number_of_threads_input = QLineEdit()
        ipqueue_description_input = QLineEdit()

        fields = [
            (ipqueue_input, "Queue:"),
            (ipqueue_errorqueue_input, "Error Queue:"),
            (ipqueue_number_of_threads_input, "Number of Threads:"),
            (ipqueue_description_input, "Description:")
        ]

        for field, label in fields:
            field.setFixedWidth(500)
            field.setFixedHeight(30)
            entry_layout.addRow(label, field)

        self.ipqueue_fields.append({
            "queue": ipqueue_input,
            "errorQueue": ipqueue_errorqueue_input,
            "numberOfThreads": ipqueue_number_of_threads_input,
            "description": ipqueue_description_input
        })

        return entry_layout
    
    def populate_ipqueue_fields_from_db(self):
        ipqueue_entries = self.get_ipqueue_data()
        for entry, field_group in zip(ipqueue_entries, self.ipqueue_fields):
            field_group["queue"].setProperty("ipqueue_id", entry["id"])
            field_group["errorQueue"].setProperty("ipqueue_id", entry["id"])
            field_group["numberOfThreads"].setProperty("ipqueue_id", entry["id"])
            field_group["description"].setProperty("ipqueue_id", entry["id"])

            field_group["queue"].setText(entry["queue"])
            field_group["errorQueue"].setText(entry["errorQueue"])
            field_group["numberOfThreads"].setText(entry["numberOfThreads"])
            field_group["description"].setText(entry["description"])

    def get_ipqueue_data(self):
        conn = self.conn_manager.get_db_connection()
        cursor = conn.cursor()
        cursor = select_from_ipqueue(cursor, self.config_manager.config_id)
        rows = cursor.fetchall()
        conn.close()
        return rows

    def save_ipqueue_fields_to_db(self, cursor):
        for field_group in self.ipqueue_fields:
            ipqueue_id = field_group["queue"].property("ipqueue_id")

            ipqueue_data = {
                "ipqueue_id": ipqueue_id,
                "queue": field_group["queue"].text(),
                "errorQueue": field_group["errorQueue"].text(),
                "numberOfThreads": field_group["numberOfThreads"].text(),
                "description": field_group["description"].text(),
                "basicConfig_id": self.config_manager.config_id
            }

            update_ipqueue(cursor, ipqueue_data)

        return cursor   

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

    def save_mqtrigger_fields_to_db(self, cursor):
        mqtrigger_data = {
            "success_interval": self.success_interval_input.text(),
            "trigger_interval": self.trigger_interval_input.text(),
            "polling": self.polling_input.text(),
            "dynamic_instance_management": self.dynamic_instance_management_input.text(),
            "dynamic_success_count": self.dynamic_success_count_input.text(),
            "dynamic_success_interval": self.dynamic_success_interval_input.text(),
            "dynamic_max_instances": self.dynamic_max_instances_input.text(),
            "basicConfig_id": self.config_manager.config_id
        }

        update_mqtrigger(cursor, mqtrigger_data)
        return cursor

    def save_fields_to_db(self):
        try:
            conn = self.conn_manager.get_db_connection()
            cursor = conn.cursor()
            self.save_mqconfig_fields_to_db(cursor)
            self.save_mqtrigger_fields_to_db(cursor)
            self.save_ipqueue_fields_to_db(cursor)
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
            self.populate_mqtrigger_fields_from_db()
            self.populate_ipqueue_fields_from_db()
        except Exception as e:
            print(f"Error populating fields from database: {e}")
            self.popup_message.show_message("Error populating fields from database.")

    def refresh_page(self):
        self.clear_layout(self.scroll_layout)
        self.create_mqconfig_layout(self.scroll_layout)
        self.add_groupbox_spacing(self.scroll_layout)
        self.create_mqtrigger_layout(self.scroll_layout)
        self.add_groupbox_spacing(self.scroll_layout)
        self.create_ipqueue_layout(self.scroll_layout)
        self.repaint()

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
