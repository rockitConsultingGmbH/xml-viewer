from PyQt5.QtWidgets import QGroupBox, QFormLayout, QLineEdit, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont
from common.config_manager import ConfigManager
from common.connection_manager import ConnectionManager
from database.utils import select_from_mqtrigger, update_mqtrigger


class MQTriggerConfiguration:
    def __init__(self):
        self.conn_manager = ConnectionManager()
        self.config_manager = ConfigManager()

        self.inputs = {
            "success_interval": QLineEdit(),
            "trigger_interval": QLineEdit(),
            "polling": QLineEdit(),
            "dynamic_instance_management": QLineEdit(),
            "dynamic_success_count": QLineEdit(),
            "dynamic_success_interval": QLineEdit(),
            "dynamic_max_instances": QLineEdit()
        }

    def create_mqtrigger_layout(self, parent_layout):
        mqtrigger_group = QGroupBox("MQTrigger Settings")
        mqtrigger_group.setObjectName("group-border")
        mqtrigger_layout = QFormLayout()

        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        mqtrigger_layout.addItem(spacer)

        self.add_mqtrigger_fields_to_form_layout(mqtrigger_layout)
        self.populate_mqtrigger_fields_from_db()

        mqtrigger_group.setLayout(mqtrigger_layout)
        parent_layout.addWidget(mqtrigger_group)

    def add_mqtrigger_fields_to_form_layout(self, form_layout):
        labels = {
            "success_interval": "Success Interval:",
            "trigger_interval": "Trigger Interval:",
            "polling": "Polling:",
            "dynamic_instance_management": "Dynamic Instance Management:",
            "dynamic_success_count": "Dynamic Success Count:",
            "dynamic_success_interval": "Dynamic Success Interval:",
            "dynamic_max_instances": "Dynamic Max Instances:"
        }

        for key, field in self.inputs.items():
            field.setFixedWidth(500)
            field.setFixedHeight(35)
            form_layout.addRow(labels[key], field)

    def populate_mqtrigger_fields_from_db(self):
        data = self.get_mqtrigger_data()
        if data:
            for key, field in self.inputs.items():
                field.setText(data.get(key, ""))

    def get_mqtrigger_data(self):
        conn = self.conn_manager.get_db_connection()
        cursor = conn.cursor()
        cursor = select_from_mqtrigger(cursor, self.config_manager.config_id)
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def save_mqtrigger_fields_to_db(self, cursor):
        mqtrigger_data = {key: field.text() for key, field in self.inputs.items()}
        mqtrigger_data["basicConfig_id"] = self.config_manager.config_id

        update_mqtrigger(cursor, mqtrigger_data)
        return cursor
