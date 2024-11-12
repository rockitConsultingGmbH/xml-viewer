from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QSpacerItem, QSizePolicy, QFormLayout, QLineEdit
from PyQt5.QtGui import QFont
from common.config_manager import ConfigManager
from common.connection_manager import ConnectionManager
from database.utils import  update_ipqueue, select_from_ipqueue

class IPQueueConfiguration:
    def __init__(self):
        self.conn_manager = ConnectionManager()
        self.config_manager = ConfigManager()
        self.ipqueue_fields = []

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