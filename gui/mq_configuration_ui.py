from PyQt5.QtWidgets import (QVBoxLayout, QFormLayout, QCheckBox,
                             QLineEdit, QWidget, QScrollArea)
from common import config_manager
from common.connection_manager import ConnectionManager
from database.utils import select_from_ipqueue, select_from_mqconfig, select_from_mqtrigger, update_ipqueue, update_mqconfig, update_mqtrigger
from gui.popup_message_ui import PopupMessage
from gui.common_components.buttons import ButtonFactory

class MQConfigurationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.conn_manager = ConnectionManager().get_instance()
        self.popup_message = PopupMessage(self)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Initialize buttons and add them at the top
        button_layout = ButtonFactory().create_button_layout(self)
        layout.addLayout(button_layout)

        # Create and add the form layout
        #form_layout = QFormLayout()
        #self.init_input_fields()
        #self.add_fields_to_form_layout(form_layout)
        #self.populate_fields_from_db()
        #layout.addLayout(form_layout)

       # Create and add the separate form layouts for MQConfig, MQTrigger, and IPQueue
        self.create_mqconfig_layout(layout)
        self.create_mqtrigger_layout(layout)
        self.create_ipqueue_layout(layout) 
        #self.set_input_field_sizes()

        self.setLayout(layout)

    def create_mqconfig_layout(self, parent_layout):
        # MQConfig Layout
        mqconfig_layout = QFormLayout()
        self.init_mqconfig_input_fields()
        self.add_mqconfig_fields_to_form_layout(mqconfig_layout)
        self.populate_mqconfig_fields_from_db()
        parent_layout.addLayout(mqconfig_layout)

    def create_mqtrigger_layout(self, parent_layout):
        # MQTrigger Layout
        mqtrigger_layout = QFormLayout()
        self.init_mqtrigger_input_fields()
        self.add_mqtrigger_fields_to_form_layout(mqtrigger_layout)
        self.populate_mqtrigger_fields_from_db()
        parent_layout.addLayout(mqtrigger_layout)

    def create_ipqueue_layout(self, parent_layout):
        # IPQueue Layout

        # IPQueue Layouts
        ipqueue_layout = QVBoxLayout()  # Create a vertical layout to hold all IPQueue entries
        ipqueue_entries = self.get_ipqueue_data()

        # Loop through each entry and create a form layout for it
        for entry in ipqueue_entries:
            entry_layout = QFormLayout()
            #self.init_ipqueue_input_fields()
            self.add_ipqueue_fields_to_form_layout(entry_layout, entry)
            #self.populate_ipqueue_fields_from_db()
            ipqueue_layout.addLayout(entry_layout)

        # Wrap the layout in a scroll area if needed
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(QWidget())
        scroll_area.widget().setLayout(ipqueue_layout)
        parent_layout.addWidget(scroll_area)

    def init_input_fields(self):
        try:
            self.init_mqconfig_input_fields()
            self.init_mqtrigger_input_fields()
            self.init_ipqueue_input_fields()
            #self.create_mqconfig_layout(layout)
            #self.create_mqtrigger_layout(layout)
            #self.create_ipqueue_layout(layout)
            self.set_input_field_sizes()
        except Exception as e:
            print(f"Error initializing input fields: {e}")
            self.popup_message.show_message("Error initializing input fields.")

    def set_fields_from_db(self):
        try:
            self.populate_mqconfig_fields_from_db()
            self.populate_mqtrigger_fields_from_db()
            self.populate_ipqueue_fields_from_db()
        except Exception as e:
            print(f"Error populating fields from database: {e}")
            self.popup_message.show_message("Error populating fields from database.")

    def save_fields_to_db(self):
        try:
            conn = self.conn_manager.get_db_connection()
            cursor = conn.cursor()
            self.save_mqconfig_fields_to_db(cursor)
            self.save_mqtrigger_fields_to_db(cursor)
            self.save_ipqueue_fields_to_db(cursor)
            conn.commit()
            self.popup_message.show_message("Changes in MQ Configuration have been successfully saved.")
        except Exception as e:
            print(f"Error while saving data: {e}")
            conn.rollback()
            self.popup_message.show_error_message(f"Error while saving data: {e}")
        finally:
            conn.close()

    def set_input_field_sizes(self):
        input_fields = [
            self.qmgr_input, self.hostname_input, self.port_input, self.channel_input,
            self.userid_input, self.password_input, self.cipher_input, self.sslPeer_input,
            self.ccsid_input, self.queue_input, self.number_of_threads_input,
            self.error_queue_input, self.command_queue_input, self.command_reply_queue_input,
            self.wait_interval_input, self.success_interval_input, self.trigger_interval_input,
            self.polling_input, self.dynamic_instance_management_input, self.dynamic_success_count_input,
            self.dynamic_success_interval_input, self.dynamic_max_instances_input,
            self.ipqueue_input, self.ipqueue_errorqueue_input, self.ipqueue_number_of_threads_input,
            self.ipqueue_description_input
        ]
        for field in input_fields:
            field.setFixedSize(500, 35)


    # MQConfig
    def init_mqconfig_input_fields(self):
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

    def add_fields_to_form_layout(self, form_layout):
        self.add_mqconfig_fields_to_form_layout(form_layout)
        self.add_mqtrigger_fields_to_form_layout(form_layout)
        self.add_ipqueue_fields_to_form_layout(form_layout)

    def add_mqconfig_fields_to_form_layout(self, form_layout):
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

    def add_mqtrigger_fields_to_form_layout(self, form_layout):
        form_layout.addRow("Success Interval:", self.success_interval_input)
        form_layout.addRow("Trigger Interval:", self.trigger_interval_input)
        form_layout.addRow("Polling:", self.polling_input)
        form_layout.addRow("Dynamic Instance Management:", self.dynamic_instance_management_input)
        form_layout.addRow("Dynamic Success Count:", self.dynamic_success_count_input)
        form_layout.addRow("Dynamic Success Interval:", self.dynamic_success_interval_input)
        form_layout.addRow("Dynamic Max Instances:", self.dynamic_max_instances_input)

    def add_ipqueue_fields_to_form_layout(self, form_layout, entry):
        # Add input fields for a single IPQueue entry
        ipqueue_input = QLineEdit(entry["queue"])
        ipqueue_errorqueue_input = QLineEdit(entry["errorQueue"])
        ipqueue_number_of_threads_input = QLineEdit(entry["numberOfThreads"])
        ipqueue_description_input = QLineEdit(entry["description"])

        form_layout.addRow("Queue:", ipqueue_input)
        form_layout.addRow("Error Queue:", ipqueue_errorqueue_input)
        form_layout.addRow("Number of Threads:", ipqueue_number_of_threads_input)
        form_layout.addRow("Description:", ipqueue_description_input)

    #def add_ipqueue_fields_to_form_layout(self, form_layout):
        #form_layout.addRow("Queue:", self.ipqueue_input)
        #form_layout.addRow("Error Queue:", self.ipqueue_errorqueue_input)
        #form_layout.addRow("Number of Threads:", self.ipqueue_number_of_threads_input)
        #form_layout.addRow("Description:", self.ipqueue_description_input)

    def get_mqconfig_data(self):
        conn = self.conn_manager.get_db_connection()
        cursor = conn.cursor()
        cursor = select_from_mqconfig(cursor, config_manager.config_id)
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

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
            "description": '',
            "basicConfig_id": config_manager.config_id
        }

        update_mqconfig(cursor, mqconfig_data)
        return cursor


    # MQTrigger
    def init_mqtrigger_input_fields(self):
        self.success_interval_input = QLineEdit()
        self.trigger_interval_input = QLineEdit()
        self.polling_input = QLineEdit()
        self.dynamic_instance_management_input = QLineEdit()
        self.dynamic_success_count_input = QLineEdit()
        self.dynamic_success_interval_input = QLineEdit()
        self.dynamic_max_instances_input = QLineEdit()

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
        cursor = select_from_mqtrigger(cursor, config_manager.config_id)
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def save_mqtrigger_fields_to_db(self, cursor):
        mqtrigger_data = {
            "success_interval": self.success_interval_input.text(),
            "trigger_interval": self.trigger_interval_input.text(),
            "polling": self.polling_input.text(),
            "dynamic_instance_management": self.dynamic_instance_management_input.text(),
            "dynamic_success_count": self.dynamic_success_count_input.text(),
            "dynamic_success_interval": self.dynamic_success_interval_input.text(),
            "dynamic_max_instances": self.dynamic_max_instances_input.text(),
            "basicConfig_id": config_manager.config_id
        }

        update_mqtrigger(cursor, mqtrigger_data)
        return cursor
        

    # IPQueue
    def init_ipqueue_input_fields(self):
        self.ipqueue_input = QLineEdit()
        self.ipqueue_errorqueue_input = QLineEdit()
        self.ipqueue_number_of_threads_input = QLineEdit()
        self.ipqueue_description_input = QLineEdit()


    def populate_ipqueue_fields_from_db(self):
        data = self.get_ipqueue_data()
        if data:
            self.ipqueue_input.setText(data["queue"])
            self.ipqueue_errorqueue_input.setText(data["errorQueue"])
            self.ipqueue_number_of_threads_input.setText(data["numberOfThreads"])
            self.ipqueue_description_input.setText(data["description"])

    def get_ipqueue_data(self):
        conn = self.conn_manager.get_db_connection()
        cursor = conn.cursor()
        cursor = select_from_ipqueue(cursor, config_manager.config_id)
        rows = cursor.fetchall()
        conn.close()
        return rows #dict(row) if row else None

    def save_ipqueue_fields_to_db(self, cursor):
        ipqueue_data = {
            "queue": self.ipqueue_input.text(),
            "errorQueue": self.ipqueue_errorqueue_input.text(),
            "numberOfThreads": self.ipqueue_number_of_threads_input.text(),
            "description": self.ipqueue_description_input.text(),
            "basicConfig_id": config_manager.config_id
        }

        update_ipqueue(cursor, ipqueue_data)
        return cursor
