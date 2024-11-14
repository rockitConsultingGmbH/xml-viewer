from PyQt5.QtWidgets import QLabel, QLineEdit, QHBoxLayout, QFormLayout, QSpacerItem, QSizePolicy, QWidget
import logging
from common.connection_manager import ConnectionManager
from common.config_manager import ConfigManager
from controllers.utils.get_and_set_value import set_text_field
from database.utils import select_from_communication

logging.basicConfig(level=logging.DEBUG)

class PatternGroup(QWidget):
    def __init__(self, group_layout, communication_id, parent_widget=None):
        super().__init__(parent_widget)
        self.communication_id = communication_id
        self.group_layout = group_layout
        self.parent_widget = parent_widget
        self.conn_manager = ConnectionManager()
        self.config_manager = ConfigManager()
        self.form_layout_left = QFormLayout()
        self.form_layout_right = QFormLayout()
        self.pattern_inputs = {}

    def setup_ui(self):
        self.group_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        hbox_left_column = QHBoxLayout()
        hbox_left_column.addItem(QSpacerItem(125, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))
        hbox_left_column.addLayout(self.form_layout_left)

        self.add_pattern(self.form_layout_left, "findPattern", "find_pattern_input", 120)
        self.add_pattern(self.form_layout_left, "quitPattern", "quit_pattern_input", 120)
        self.add_pattern(self.form_layout_left, "ackPattern", "ack_pattern_input", 120)
        self.add_pattern(self.form_layout_left, "zipPattern", "zip_pattern_input", 120)

        hbox_columns = QHBoxLayout()
        hbox_columns.addLayout(hbox_left_column)
        hbox_columns.addStretch(1)
        hbox_columns.addLayout(self.form_layout_right)

        self.add_pattern(self.form_layout_right, "movPattern", "mov_pattern_input", 120)
        self.add_pattern(self.form_layout_right, "putPattern", "put_pattern_input", 120)
        self.add_pattern(self.form_layout_right, "rcvPattern", "rcv_pattern_input", 120)
        self.add_pattern(self.form_layout_right, "tmpPattern", "tmp_pattern_input", 120)

        self.group_layout.addLayout(hbox_columns)
        self.group_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        self.populate_patterns(self.communication_id)

    def add_pattern(self, layout, label_text, input_name, label_width):
        pattern_label = QLabel(label_text)
        pattern_label.setFixedWidth(label_width)
        pattern_input = QLineEdit()
        pattern_input.setObjectName(input_name)
        pattern_input.setFixedSize(450, 30)
        layout.addRow(pattern_label, pattern_input)
        self.pattern_inputs[input_name] = pattern_input

    def populate_patterns(self, communication_id):
        conn = self.conn_manager.get_db_connection()
        cursor = conn.cursor()

        row = select_from_communication(cursor, communication_id, self.config_manager.config_id).fetchone()

        if row:
            logging.debug("Data fetched for communication_id: %s", communication_id)
            logging.debug("Populating patterns...")

            pattern_names = [
                "find_pattern_input", "quit_pattern_input", "ack_pattern_input",
                "zip_pattern_input", "mov_pattern_input", "put_pattern_input", "rcv_pattern_input",
                "tmp_pattern_input"
            ]

            pattern_values = [
                row['findPattern'], row['quitPattern'], row['ackPattern'],
                row['zipPattern'], row['movPattern'], row['putPattern'], row['rcvPattern'],
                row['tmpPattern']
            ]

            for pattern_name, pattern_value in zip(pattern_names, pattern_values):
                if pattern_name in self.pattern_inputs:
                    self.pattern_inputs[pattern_name].setText(pattern_value)
                else:
                    logging.warning(f"Pattern input {pattern_name} not found in pattern_inputs dictionary.")
        else:
            logging.warning("No data found for communication_id: %s", communication_id)
        conn.close()

    def reset_ui(self):
        self.populate_patterns(self.communication_id)
