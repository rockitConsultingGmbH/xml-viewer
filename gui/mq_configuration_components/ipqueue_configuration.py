from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QSpacerItem, QSizePolicy, QFormLayout, QLineEdit, QWidget, QPushButton, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from common.config_manager import ConfigManager
from common.connection_manager import ConnectionManager
from database.utils import update_ipqueue, select_from_ipqueue, insert_into_ipqueue

class IPQueueConfiguration:
    def __init__(self):
        self.conn_manager = ConnectionManager()
        self.config_manager = ConfigManager()
        self.ipqueue_fields = []
        self.new_ipqueues = []
        self.ipqueue_main_layout = None

    def create_ipqueue_layout(self, parent_layout):
        ipqueue_group = QGroupBox("IPQueue Settings")
        ipqueue_group.setObjectName("group-border")
        ipqueue_group.setFont(QFont("Arial", 12, QFont.Bold))
        ipqueue_group.setStyleSheet("QLabel { border: none; font-size: 12px; } QLineEdit, QCheckBox { font-size: 12px; }")
        
        self.ipqueue_main_layout = QVBoxLayout()

        ipqueues_label_row_layout = QHBoxLayout()
        ipqueues_label_row_layout.setAlignment(Qt.AlignLeft)
        
        self.ipqueue_main_layout.addItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Fixed))

        ipqueues_label = QLabel("IPQueues")
        font = QFont()
        font.setBold(True)
        ipqueues_label.setFont(font)
        ipqueues_label.setFixedWidth(110)
        ipqueues_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        ipqueue_add_button = QPushButton("+")
        ipqueue_add_button.setObjectName("addButton")
        ipqueue_add_button.setFixedSize(30, 30)
        ipqueue_add_button.clicked.connect(lambda: self.add_ipqueue_to_layout(new=True))

        ipqueues_label_row_layout.addWidget(ipqueues_label)
        ipqueues_label_row_layout.addWidget(ipqueue_add_button)
        
        ipqueues_label_row_layout.addStretch()
        self.ipqueue_main_layout.addLayout(ipqueues_label_row_layout)
        self.ipqueue_main_layout.addItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Load and display IPQueue entries in ascending order of ID (oldest first)
        ipqueue_entries = sorted(self.get_ipqueue_data(), key=lambda x: x['id'])
        for entry in ipqueue_entries:
            self.add_ipqueue_to_layout(entry)

        ipqueue_group.setLayout(self.ipqueue_main_layout)
        parent_layout.addWidget(ipqueue_group)

    def add_ipqueue_to_layout(self, entry=None, new=False):
        ipqueue_id = entry["id"] if entry else None
        
        individual_ipqueue_group = QWidget()
        individual_ipqueue_layout = QFormLayout()

        ipqueue_input_label = QLabel("Queue:")
        font = QFont()
        font.setBold(True)
        ipqueue_input_label.setFont(font)
        ipqueue_input_label.setFixedWidth(110)
        ipqueue_input_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        ipqueue_input = QLineEdit(entry["queue"] if entry else "")
        ipqueue_input.setFixedSize(500, 30)
        ipqueue_input.setProperty("ipqueue_id", ipqueue_id)
        
        ipqueue_delete_button = QPushButton("-")
        ipqueue_delete_button.setObjectName("deleteButton")
        ipqueue_delete_button.setFixedSize(30, 30)
        ipqueue_delete_button.clicked.connect(lambda: self.delete_ipqueue(individual_ipqueue_group, ipqueue_id))

        ipqueue_errorqueue_input = QLineEdit(entry["errorQueue"] if entry else "")
        ipqueue_number_of_threads_input = QLineEdit(entry["numberOfThreads"] if entry else "")
        ipqueue_description_input = QLineEdit(entry["description"] if entry else "")

        fields = [
            (ipqueue_errorqueue_input, "Error Queue:"),
            (ipqueue_number_of_threads_input, "Number of Threads:"),
            (ipqueue_description_input, "Description:")
        ]

        target_row_layout = QHBoxLayout()
        target_row_layout.setAlignment(Qt.AlignLeft)
        target_row_layout.addWidget(ipqueue_input_label)
        target_row_layout.addWidget(ipqueue_input)
        target_row_layout.addWidget(ipqueue_delete_button)

        individual_ipqueue_layout.addRow(target_row_layout)

        for field, label in fields:
            field.setFixedWidth(500)
            field.setFixedHeight(30)
            individual_ipqueue_layout.addRow(label, field)

        ipqueue_entry = {
            "queue": ipqueue_input,
            "errorQueue": ipqueue_errorqueue_input,
            "numberOfThreads": ipqueue_number_of_threads_input,
            "description": ipqueue_description_input,
            "id": ipqueue_id
        }
        self.ipqueue_fields.append(ipqueue_entry)

        if new:
            self.new_ipqueues.append(ipqueue_entry)

        individual_ipqueue_group.setLayout(individual_ipqueue_layout)

        if new:
            self.ipqueue_main_layout.insertWidget(2, individual_ipqueue_group)
        else:
            self.ipqueue_main_layout.addWidget(individual_ipqueue_group)

    def delete_ipqueue(self, ipqueue_widget, ipqueue_id):
        """Remove an IPQueue from the layout and mark for deletion if it exists in the DB."""
        if ipqueue_id:
            self.ipqueue_fields = [field for field in self.ipqueue_fields if field["id"] != ipqueue_id]
            # Here, you would also add the logic to handle the actual DB deletion when saving
        # Remove widget from UI
        ipqueue_widget.setParent(None)

    def populate_ipqueue_fields_from_db(self):
        ipqueue_entries = self.get_ipqueue_data()
        for entry, field_group in zip(ipqueue_entries, self.ipqueue_fields):
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
        return [{"id": row["id"], "queue": row["queue"], "errorQueue": row["errorQueue"], "numberOfThreads": row["numberOfThreads"], "description": row["description"]} for row in rows]

    def save_ipqueue_fields_to_db(self, cursor):
        for field_group in self.ipqueue_fields:
            ipqueue_id = field_group["id"]
            ipqueue_data = {
                "queue": field_group["queue"].text(),
                "errorQueue": field_group["errorQueue"].text(),
                "numberOfThreads": field_group["numberOfThreads"].text(),
                "description": field_group["description"].text(),
                "basicConfig_id": self.config_manager.config_id,
                "mqConfig_id": self.config_manager.mqconfig_id
            }

            if ipqueue_id:
                ipqueue_data["ipqueue_id"] = ipqueue_id
                update_ipqueue(cursor, ipqueue_data)
            else:
                ipqueue_id = insert_into_ipqueue(cursor, ipqueue_data)
                field_group["id"] = ipqueue_id

        return cursor
