from PyQt5.QtWidgets import QLabel, QLineEdit, QHBoxLayout, QFormLayout, QSpacerItem, QSizePolicy, QFrame


def create_pattern_group(group_layout):
    form_layout_left = QFormLayout()
    form_layout_right = QFormLayout()

    group_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

    hbox_left_column = QHBoxLayout()
    hbox_left_column.addItem(QSpacerItem(125, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))
    hbox_left_column.addLayout(form_layout_left)

    pattern_label1 = QLabel("findPattern")
    pattern_label1.setFixedWidth(100)
    pattern_input1 = QLineEdit()
    pattern_input1.setObjectName("find_pattern_input")
    pattern_input1.setFixedSize(450, 30)
    form_layout_left.addRow(pattern_label1, pattern_input1)

    pattern_label2 = QLabel("quitPattern")
    pattern_label2.setFixedWidth(100)
    pattern_input2 = QLineEdit()
    pattern_input2.setObjectName("quit_pattern_input")
    pattern_input2.setFixedSize(450, 30)
    form_layout_left.addRow(pattern_label2, pattern_input2)

    pattern_label3 = QLabel("ackPattern")
    pattern_label3.setFixedWidth(100)
    pattern_input3 = QLineEdit()
    pattern_input3.setObjectName("ack_pattern_input")
    pattern_input3.setFixedSize(450, 30)
    form_layout_left.addRow(pattern_label3, pattern_input3)

    pattern_label4 = QLabel("zipPattern")
    pattern_label4.setFixedWidth(100)
    pattern_input4 = QLineEdit()
    pattern_input4.setObjectName("zip_pattern_input")
    pattern_input4.setFixedSize(450, 30)
    form_layout_left.addRow(pattern_label4, pattern_input4)

    pattern_label5 = QLabel("movPattern")
    pattern_label5.setFixedWidth(120)
    pattern_input5 = QLineEdit()
    pattern_input5.setObjectName("mov_pattern_input")
    pattern_input5.setFixedSize(450, 30)
    form_layout_right.addRow(pattern_label5, pattern_input5)

    pattern_label6 = QLabel("putPattern")
    pattern_label6.setFixedWidth(120)
    pattern_input6 = QLineEdit()
    pattern_input6.setObjectName("put_pattern_input")
    pattern_input6.setFixedSize(450, 30)
    form_layout_right.addRow(pattern_label6, pattern_input6)

    pattern_label7 = QLabel("rcvPattern")
    pattern_label7.setFixedWidth(120)
    pattern_input7 = QLineEdit()
    pattern_input7.setObjectName("rcv_pattern_input")
    pattern_input7.setFixedSize(450, 30)
    form_layout_right.addRow(pattern_label7, pattern_input7)

    pattern_label8 = QLabel("tmpPattern")
    pattern_label8.setFixedWidth(120)
    pattern_input8 = QLineEdit()
    pattern_input8.setObjectName("tmp_pattern_input")
    pattern_input8.setFixedSize(450, 30)
    form_layout_right.addRow(pattern_label8, pattern_input8)

    hbox_columns = QHBoxLayout()
    hbox_columns.addLayout(hbox_left_column)
    hbox_columns.addStretch()
    hbox_columns.addLayout(form_layout_right)

    group_layout.addLayout(hbox_columns)

