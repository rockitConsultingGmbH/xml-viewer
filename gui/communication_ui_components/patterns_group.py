from PyQt5.QtWidgets import QLabel, QLineEdit, QHBoxLayout, QFormLayout, QSpacerItem, QSizePolicy, QFrame

class PatternGroup:
    def __init__(self, group_layout, communication_id):
        self.communication_id = communication_id
        self.group_layout = group_layout
        self.form_layout_left = QFormLayout()
        self.form_layout_right = QFormLayout()

    def create_pattern_group(self):
        self.group_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        hbox_left_column = QHBoxLayout()
        hbox_left_column.addItem(QSpacerItem(125, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))
        hbox_left_column.addLayout(self.form_layout_left)
        hbox_left_column.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))  # Spacer

        self.add_pattern(self.form_layout_left, "findPattern", "find_pattern_input", 100)
        self.add_pattern(self.form_layout_left, "quitPattern", "quit_pattern_input", 100)
        self.add_pattern(self.form_layout_left, "ackPattern", "ack_pattern_input", 100)
        self.add_pattern(self.form_layout_left, "zipPattern", "zip_pattern_input", 100)
        self.add_pattern(self.form_layout_right, "movPattern", "mov_pattern_input", 120)
        self.add_pattern(self.form_layout_right, "putPattern", "put_pattern_input", 120)
        self.add_pattern(self.form_layout_right, "rcvPattern", "rcv_pattern_input", 120)
        self.add_pattern(self.form_layout_right, "tmpPattern", "tmp_pattern_input", 120)

        hbox_columns = QHBoxLayout()
        hbox_columns.addLayout(hbox_left_column)
        hbox_columns.addStretch()
        hbox_columns.addLayout(self.form_layout_right)

        self.group_layout.addLayout(hbox_columns)

    def add_pattern(self, layout, label_text, input_name, label_width):
        pattern_label = QLabel(label_text)
        pattern_label.setFixedWidth(label_width)
        pattern_input = QLineEdit()
        pattern_input.setObjectName(input_name)
        pattern_input.setFixedSize(450, 30)
        layout.addRow(pattern_label, pattern_input)
