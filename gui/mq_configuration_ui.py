from PyQt5.QtWidgets import (QVBoxLayout, QFormLayout, QCheckBox, QLineEdit, QWidget, QScrollArea, QGroupBox, QSpacerItem, QSizePolicy, QFrame)
from PyQt5.QtGui import QFont
from common import config_manager
from common.connection_manager import ConnectionManager
from database.utils import select_from_ipqueue, select_from_mqconfig, select_from_mqtrigger, update_ipqueue, update_mqconfig, update_mqtrigger
from gui.components.popup_message_ui import PopupMessage
from gui.components.buttons import ButtonFactory

class MQConfigurationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.conn_manager = ConnectionManager().get_instance()
        self.popup_message = PopupMessage(self)
        self.ipqueue_fields = []  # Store references to the input fields for saving   
        self.setup_ui()

    def setup_ui(self):
        # Create the main layout
        main_layout = QVBoxLayout(self)

        # Initialize buttons and add them at the top
        button_layout = ButtonFactory().create_button_layout(self)
        main_layout.addLayout(button_layout)

        # Create scroll area
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        #self.scroll_area.setStyleSheet("QScrollArea { border: none; } QWidget { border: none; } "
        #                      "QLineEdit, QComboBox, QPushButton { border: 1px solid gray; }")
        #self.scroll_area.setStyleSheet("QLineEdit { border: 1px solid gray; }")
        self.scroll_area.setFrameShape(QFrame.NoFrame)

        scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_content)

        # Create and add separate form layouts for MQConfig, MQTrigger, and IPQueue
        self.create_mqconfig_layout(self.scroll_layout)
        self.add_spacing(self.scroll_layout)
        self.create_mqtrigger_layout(self.scroll_layout)
        self.add_spacing(self.scroll_layout)
        self.create_ipqueue_layout(self.scroll_layout)

        self.scroll_area.setWidget(scroll_content)
        main_layout.addWidget(self.scroll_area)
        self.setLayout(main_layout)

    # Add spacing method
    def add_spacing(self, layout):
        spacer = QSpacerItem(30, 100, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)

    # MQConfig Layout
    def create_mqconfig_layout(self, parent_layout):
        mqconfig_group = QGroupBox("MQ Configuration")
        mqconfig_group.setFont(QFont("Arial", 10, QFont.Bold))
        mqconfig_layout = QFormLayout()

        self.add_mqconfig_fields_to_form_layout(mqconfig_layout)
        self.populate_mqconfig_fields_from_db()
        mqconfig_group.setLayout(mqconfig_layout)
        parent_layout.addWidget(mqconfig_group)

    def add_mqconfig_fields_to_form_layout(self, form_layout):
        #font = QFont("Arial", 10)

        # Input fields with larger font and size
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

        # Apply the larger font to input fields
        for field in [self.qmgr_input, self.hostname_input, self.port_input, self.channel_input, self.userid_input,
                      self.password_input, self.cipher_input, self.sslPeer_input, self.ccsid_input, self.queue_input,
                      self.number_of_threads_input, self.error_queue_input, self.command_queue_input, self.command_reply_queue_input,
                      self.wait_interval_input]:
            #field.setFont(font)
            field.setFixedWidth(500)
            field.setFixedHeight(35)

        # Add rows with larger fonts for labels
        form_layout.addRow("Remote:", self.is_remote_input)
        form_layout.addRow("Queue Manager:", self.qmgr_input)
        form_layout.addRow("Hostname:", self.hostname_input)
        form_layout.addRow("Port:", self.port_input)
        form_layout.addRow("Channel:", self.channel_input)
        form_layout.addRow("User ID:", self.userid_input)
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
        cursor = select_from_mqconfig(cursor, config_manager.config_id)
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    # MQTrigger Layout
    def create_mqtrigger_layout(self, parent_layout):
        mqtrigger_group = QGroupBox("MQTrigger Settings")
        mqtrigger_group.setFont(QFont("Arial", 10, QFont.Bold))
        mqtrigger_layout = QFormLayout()

        self.add_mqtrigger_fields_to_form_layout(mqtrigger_layout)
        self.populate_mqtrigger_fields_from_db()

        mqtrigger_group.setLayout(mqtrigger_layout)
        parent_layout.addWidget(mqtrigger_group)

    def add_mqtrigger_fields_to_form_layout(self, form_layout):
        #font = QFont("Arial", 10)  # Larger font for labels and input fields

        # Input fields with larger font and size
        self.success_interval_input = QLineEdit()
        self.trigger_interval_input = QLineEdit()
        self.polling_input = QLineEdit()
        self.dynamic_instance_management_input = QLineEdit()
        self.dynamic_success_count_input = QLineEdit()
        self.dynamic_success_interval_input = QLineEdit()
        self.dynamic_max_instances_input = QLineEdit()

        for field in [self.success_interval_input, self.trigger_interval_input, self.polling_input,
                      self.dynamic_instance_management_input, self.dynamic_success_count_input,
                      self.dynamic_success_interval_input, self.dynamic_max_instances_input]:
            #field.setFont(font)
            field.setFixedWidth(500)
            field.setFixedHeight(35)

        # Add rows with larger fonts for labels
        form_layout.addRow("Success Interval:", self.success_interval_input)
        form_layout.addRow("Trigger Interval:", self.trigger_interval_input)
        form_layout.addRow("Polling:", self.polling_input)
        form_layout.addRow("Dynamic Instance Management:", self.dynamic_instance_management_input)
        form_layout.addRow("Dynamic Success Count:", self.dynamic_success_count_input)
        form_layout.addRow("Dynamic Success Interval:", self.dynamic_success_interval_input)
        form_layout.addRow("Dynamic Max Instances:", self.dynamic_max_instances_input)

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

    # IPQueue Layout
    def create_ipqueue_layout(self, parent_layout):
        # Main Group for IPQueue Settings
        ipqueue_group = QGroupBox("IPQueue Settings")
        ipqueue_group.setFont(QFont("Arial", 10, QFont.Bold))
        ipqueue_main_layout = QVBoxLayout()

        ipqueue_entries = self.get_ipqueue_data()

        for entry in ipqueue_entries:
            # Create a separate group for each IPQueue
            individual_ipqueue_group = QGroupBox(f"IPQueue") #QGroupBox(f"Queue: {entry['queue']}")
            individual_ipqueue_group.setFont(QFont("Arial", 8, QFont.Bold))
            individual_ipqueue_layout = QFormLayout()

            # Add the IPQueue fields
            individual_ipqueue_layout = self.add_ipqueue_fields_to_form_layout(individual_ipqueue_layout, entry)
            self.populate_ipqueue_fields_from_db()

            individual_ipqueue_group.setLayout(individual_ipqueue_layout)

            # Add some spacing between each group
            ipqueue_main_layout.addWidget(individual_ipqueue_group)
            ipqueue_main_layout.addSpacing(20)

        ipqueue_group.setLayout(ipqueue_main_layout)
        parent_layout.addWidget(ipqueue_group)

    def add_ipqueue_fields_to_form_layout(self, entry_layout, entry):
        #font = QFont("Arial", 12)

        ipqueue_input = QLineEdit()
        ipqueue_errorqueue_input = QLineEdit()
        ipqueue_number_of_threads_input = QLineEdit()
        ipqueue_description_input = QLineEdit()

        for field in [ipqueue_input, ipqueue_errorqueue_input, ipqueue_number_of_threads_input, ipqueue_description_input]:
            #field.setFont(font)
            field.setFixedWidth(500)
            field.setFixedHeight(30)

        # Add fields to the layout
        entry_layout.addRow("Queue:", ipqueue_input)
        entry_layout.addRow("Error Queue:", ipqueue_errorqueue_input)
        entry_layout.addRow("Number of Threads:", ipqueue_number_of_threads_input)
        entry_layout.addRow("Description:", ipqueue_description_input)

        # Store a reference to these fields for later saving
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
        cursor = select_from_ipqueue(cursor, config_manager.config_id)
        rows = cursor.fetchall()
        conn.close()
        return rows

    def save_ipqueue_fields_to_db(self, cursor):
        for field_group in self.ipqueue_fields:
            # Retrieve the ID from one of the input fields
            ipqueue_id = field_group["queue"].property("ipqueue_id")

            ipqueue_data = {
                "ipqueue_id": ipqueue_id,
                "queue": field_group["queue"].text(),
                "errorQueue": field_group["errorQueue"].text(),
                "numberOfThreads": field_group["numberOfThreads"].text(),
                "description": field_group["description"].text(),
                "basicConfig_id": config_manager.config_id
            }

            # Update the database for this specific IPQueue entry
            update_ipqueue(cursor, ipqueue_data)

        return cursor   

    #Save and Reset Functions
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
            "basicConfig_id": config_manager.config_id
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
            "basicConfig_id": config_manager.config_id
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
            #self.refresh_page()
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

    # Refresh page after an update
    def refresh_page(self):
        # Clear the current layout
        self.clear_layout(self.scroll_layout)

        # Rebuild the UI with updated data
        self.create_mqconfig_layout(self.scroll_layout)
        self.add_spacing(self.scroll_layout)
        self.create_mqtrigger_layout(self.scroll_layout)
        self.add_spacing(self.scroll_layout)
        self.create_ipqueue_layout(self.scroll_layout)
        
        self.repaint()

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()