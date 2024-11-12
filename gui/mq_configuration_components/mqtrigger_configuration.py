from PyQt5.QtWidgets import QGroupBox, QFormLayout, QLineEdit, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont
from common.config_manager import ConfigManager
from common.connection_manager import ConnectionManager
from database.utils import  select_from_mqtrigger, update_mqtrigger


class MQTriggerConfiguration:
    def __init__(self):
        self.conn_manager = ConnectionManager()
        self.config_manager = ConfigManager()

        self.success_interval_input = QLineEdit()
        self.trigger_interval_input = QLineEdit()
        self.polling_input = QLineEdit()
        self.dynamic_instance_management_input = QLineEdit()
        self.dynamic_success_count_input = QLineEdit()
        self.dynamic_success_interval_input = QLineEdit()
        self.dynamic_max_instances_input = QLineEdit()

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