from PyQt5.QtWidgets import QLabel, QCheckBox, QLineEdit, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy

from gui.common_components.clickable_label import ClickableLabel


class SettingsGroup:
    def __init__(self, group_layout, communication_id, toggle_inputs):
        self.communication_id = communication_id
        self.group_layout = group_layout
        self.toggle_inputs = toggle_inputs
        self.settings_labels = []
        self.settings_inputs = []
        self.other_settings_labels = []
        self.other_settings_inputs = []

    def create_settings_group(self):
        hbox = QHBoxLayout()

        self.group_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        polling_label = ClickableLabel("Polling")
        polling_label.setFixedWidth(120)
        polling_label.setObjectName("label_parent")
        hbox.addWidget(polling_label)

        poll_until_found_checkbox = QCheckBox("Poll until found")
        poll_until_found_checkbox.setObjectName("poll_until_found_checkbox")
        poll_until_found_checkbox.setFixedWidth(200)

        no_transfer_checkbox = QCheckBox("No transfer")
        no_transfer_checkbox.setObjectName("no_transfer_checkbox")

        hbox.addWidget(poll_until_found_checkbox)
        hbox.addWidget(no_transfer_checkbox)

        self.group_layout.addLayout(hbox)

        self.group_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        form_layout_left = QVBoxLayout()

        hbox_gueltig_ab = QHBoxLayout()
        hbox_gueltig_ab.addItem(QSpacerItem(125, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))
        gueltig_ab_label = QLabel("Gültig ab")
        gueltig_ab_label.setFixedWidth(100)
        gueltig_ab_input = QLineEdit()
        gueltig_ab_input.setObjectName("gueltig_ab_input")
        gueltig_ab_input.setFixedSize(450, 30)
        hbox_gueltig_ab.addWidget(gueltig_ab_label)
        hbox_gueltig_ab.addWidget(gueltig_ab_input)
        form_layout_left.addLayout(hbox_gueltig_ab)

        hbox_input1 = QHBoxLayout()
        hbox_input1.addItem(QSpacerItem(125, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))
        input1_label = QLabel("Beförderung ab")
        input1_label.setFixedWidth(100)
        input1 = QLineEdit()
        input1.setObjectName("befoerderung_ab_input")
        input1.setFixedSize(450, 30)
        hbox_input1.addWidget(input1_label)
        hbox_input1.addWidget(input1)
        form_layout_left.addLayout(hbox_input1)

        self.settings_labels.extend([gueltig_ab_label, input1_label])
        self.settings_inputs.extend([gueltig_ab_input, input1])

        hbox_input2 = QHBoxLayout()
        hbox_input2.addItem(QSpacerItem(125, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))
        input2_label = QLabel("Poll Intervall")
        input2_label.setFixedWidth(100)
        input2 = QLineEdit()
        input2.setObjectName("poll_interval_input")
        input2.setFixedSize(450, 30)
        hbox_input2.addWidget(input2_label)
        hbox_input2.addWidget(input2)
        form_layout_left.addLayout(hbox_input2)

        self.settings_labels.append(input2_label)
        self.settings_inputs.append(input2)

        form_layout_right = QVBoxLayout()

        hbox_gueltig_bis = QHBoxLayout()
        gueltig_bis_label = QLabel("Gültig bis")
        gueltig_bis_label.setFixedWidth(120)
        gueltig_bis_input = QLineEdit()
        gueltig_bis_input.setObjectName("gueltig_bis_input")
        gueltig_bis_input.setFixedSize(450, 30)
        hbox_gueltig_bis.addWidget(gueltig_bis_label)
        hbox_gueltig_bis.addWidget(gueltig_bis_input)
        form_layout_right.addLayout(hbox_gueltig_bis)

        hbox_input3 = QHBoxLayout()
        input3_label = QLabel("Beförderung bis")
        input3_label.setFixedWidth(120)
        input3 = QLineEdit()
        input3.setObjectName("befoerderung_bis_input")
        input3.setFixedSize(450, 30)
        hbox_input3.addWidget(input3_label)
        hbox_input3.addWidget(input3)
        form_layout_right.addLayout(hbox_input3)

        self.settings_labels.extend([gueltig_bis_label, input3_label])
        self.settings_inputs.extend([gueltig_bis_input, input3])

        hbox_input4 = QHBoxLayout()
        input4_label = QLabel("Escalation timeout")
        input4_label.setFixedWidth(120)
        input4 = QLineEdit()
        input4.setObjectName("escalation_timeout_input")
        input4.setFixedSize(450, 30)
        hbox_input4.addWidget(input4_label)
        hbox_input4.addWidget(input4)
        form_layout_right.addLayout(hbox_input4)

        self.settings_labels.append(input4_label)
        self.settings_inputs.append(input4)

        polling_label.mousePressEvent = lambda event: self.toggle_inputs(self.settings_labels, self.settings_inputs)

        hbox_columns = QHBoxLayout()
        hbox_columns.addLayout(form_layout_left)
        hbox_columns.addStretch()
        hbox_columns.addLayout(form_layout_right)

        self.group_layout.addLayout(hbox_columns)

        self.group_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        hbox_new_settings = QHBoxLayout()
        new_label = QLabel("Compression")
        new_label.setObjectName("label_parent")
        new_label.setFixedWidth(120)
        hbox_new_settings.addWidget(new_label)

        new_checkbox1 = QCheckBox("Pre-Unzip")
        new_checkbox1.setObjectName("pre_unzip_checkbox")
        new_checkbox1.setFixedWidth(200)
        hbox_new_settings.addWidget(new_checkbox1)

        new_checkbox2 = QCheckBox("Post-Zip")
        new_checkbox2.setObjectName("post_zip_checkbox")
        hbox_new_settings.addWidget(new_checkbox2)

        self.group_layout.addLayout(hbox_new_settings)

        self.group_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        hbox_additional_settings = QHBoxLayout()
        additional_label = QLabel("Other Settings")
        additional_label.setObjectName("label_parent")
        additional_label.setFixedWidth(120)
        hbox_additional_settings.addWidget(additional_label)

        additional_checkbox1 = QCheckBox("Rename with Timestamp")
        additional_checkbox1.setObjectName("rename_with_timestamp_checkbox")
        hbox_additional_settings.addWidget(additional_checkbox1)

        self.group_layout.addLayout(hbox_additional_settings)

        self.group_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))
