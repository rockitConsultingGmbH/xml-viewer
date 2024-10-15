from PyQt5.QtWidgets import QFormLayout, QLineEdit, QLabel
from utils.clickable_label import ClickableLabel

from utils.toggle_inputs import toggle_inputs


def create_description_form(label_style):

    form_layout_right = QFormLayout()

    description_label = ClickableLabel("Description(s)")
    description_label.setStyleSheet(label_style)

    description_input = QLineEdit()
    description_input.setObjectName("description_input")
    description_input.setFixedSize(550, 30)

    form_layout_right.addRow(description_label, description_input)

    description_1_label = QLabel("Description")
    description_1_label.setStyleSheet(label_style)
    description_1_input = QLineEdit()
    description_1_input.setFixedSize(550, 30)
    description_1_input.setObjectName("description_1_input")

    description_2_label = QLabel("Description")
    description_2_label.setStyleSheet(label_style)
    description_2_input = QLineEdit()
    description_2_input.setFixedSize(550, 30)
    description_2_input.setObjectName("description_2_input")

    description_3_label = QLabel("Description")
    description_3_label.setStyleSheet(label_style)
    description_3_input = QLineEdit()
    description_3_input.setFixedSize(550, 30)
    description_3_input.setObjectName("description_3_input")

    form_layout_right.addRow(description_1_label, description_1_input)
    form_layout_right.addRow(description_2_label, description_2_input)
    form_layout_right.addRow(description_3_label, description_3_input)

    input_labels = [description_1_label, description_2_label, description_3_label]
    input_fields = [description_1_input, description_2_input, description_3_input]

    description_label.mousePressEvent = lambda event: toggle_inputs(input_labels, input_fields)

    return form_layout_right
