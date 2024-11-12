from PyQt5.QtWidgets import QLabel, QCheckBox, QLineEdit, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QWidget, QGridLayout
from PyQt5.QtCore import Qt

from gui.common_components.clickable_label import ClickableLabel


class SettingsGroup(QWidget):
    def __init__(self, group_layout, communication_id, toggle_inputs):
        super().__init__()
        self.communication_id = communication_id
        self.group_layout = group_layout
        self.toggle_inputs = toggle_inputs
        self.settings_labels = []
        self.settings_inputs = []
        self.other_settings_labels = []
        self.other_settings_inputs = []

    def create_settings_group(self):
        hbox = QHBoxLayout()
        hbox.setAlignment(Qt.AlignLeft)

        self.group_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        polling_label = ClickableLabel("Polling")
        polling_label.setFixedWidth(120)
        polling_label.setObjectName("label_parent")
        polling_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        hbox.addWidget(polling_label)

        poll_until_found_checkbox = QCheckBox("Poll until found")
        poll_until_found_checkbox.setObjectName("poll_until_found_checkbox")
        poll_until_found_checkbox.setFixedWidth(200)
        poll_until_found_checkbox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        no_transfer_checkbox = QCheckBox("No transfer")
        no_transfer_checkbox.setObjectName("no_transfer_checkbox")
        no_transfer_checkbox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        hbox.addWidget(poll_until_found_checkbox)
        hbox.addWidget(no_transfer_checkbox)

        self.group_layout.addLayout(hbox)

        self.group_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))

        grid_layout = QGridLayout()

        # Row 0 - Gültig ab
        grid_layout.addItem(QSpacerItem(125, 0, QSizePolicy.Fixed, QSizePolicy.Minimum), 0, 0)
        gultig_ab_label = QLabel("Gültig ab")
        gultig_ab_label.setFixedWidth(120)
        gultig_ab_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        gultig_ab_input = QLineEdit()
        gultig_ab_input.setObjectName("gueltig_ab_input")
        gultig_ab_input.setFixedSize(450, 30)
        gultig_ab_input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        grid_layout.addWidget(gultig_ab_label, 0, 1, Qt.AlignLeft)
        grid_layout.addWidget(gultig_ab_input, 0, 2, Qt.AlignLeft)

        # Row 0 - Gültig bis
        grid_layout.addItem(QSpacerItem(125, 0, QSizePolicy.Fixed, QSizePolicy.Minimum), 0, 3)
        gultig_bis_label = QLabel("Gültig bis")
        gultig_bis_label.setFixedWidth(120)
        gultig_bis_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        gultig_bis_input = QLineEdit()
        gultig_bis_input.setObjectName("gueltig_bis_input")
        gultig_bis_input.setFixedSize(450, 30)
        gultig_bis_input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        grid_layout.addWidget(gultig_bis_label, 0, 4, Qt.AlignLeft)
        grid_layout.addWidget(gultig_bis_input, 0, 5, Qt.AlignLeft)

        # Row 1 - Beförderung ab
        grid_layout.addItem(QSpacerItem(125, 0, QSizePolicy.Fixed, QSizePolicy.Minimum), 1, 0)
        befoerderung_ab_label = QLabel("Beförderung ab")
        befoerderung_ab_label.setFixedWidth(120)
        befoerderung_ab_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        befoerderung_ab_input = QLineEdit()
        befoerderung_ab_input.setObjectName("befoerderung_ab_input")
        befoerderung_ab_input.setFixedSize(450, 30)
        befoerderung_ab_input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        grid_layout.addWidget(befoerderung_ab_label, 1, 1, Qt.AlignLeft)
        grid_layout.addWidget(befoerderung_ab_input, 1, 2, Qt.AlignLeft)

        # Row 1 - Beförderung bis
        grid_layout.addItem(QSpacerItem(125, 0, QSizePolicy.Fixed, QSizePolicy.Minimum), 1, 3)
        befoerderung_bis_label = QLabel("Beförderung bis")
        befoerderung_bis_label.setFixedWidth(120)
        befoerderung_bis_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        befoerderung_bis_input = QLineEdit()
        befoerderung_bis_input.setObjectName("befoerderung_bis_input")
        befoerderung_bis_input.setFixedSize(450, 30)
        befoerderung_bis_input.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        grid_layout.addWidget(befoerderung_bis_label, 1, 4, Qt.AlignLeft)
        grid_layout.addWidget(befoerderung_bis_input, 1, 5, Qt.AlignLeft)

        # Row 2 - Beförderung Cron
        grid_layout.addItem(QSpacerItem(125, 0, QSizePolicy.Fixed, QSizePolicy.Minimum), 2, 0)
        input_cron_label = QLabel("Beförderung Cron")
        input_cron_label.setFixedWidth(120)
        input_cron_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        input_cron = QLineEdit()
        input_cron.setObjectName("befoerderung_cron_input")
        input_cron.setFixedSize(450, 30)
        input_cron.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        grid_layout.addWidget(input_cron_label, 2, 1, Qt.AlignLeft)
        grid_layout.addWidget(input_cron, 2, 2, Qt.AlignLeft)

        # Row 3 - Poll Intervall
        grid_layout.addItem(QSpacerItem(125, 0, QSizePolicy.Fixed, QSizePolicy.Minimum), 3, 0)
        input2_label = QLabel("Poll Intervall")
        input2_label.setFixedWidth(120)
        input2_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        input2 = QLineEdit()
        input2.setObjectName("poll_interval_input")
        input2.setFixedSize(450, 30)
        input2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        grid_layout.addWidget(input2_label, 3, 1, Qt.AlignLeft)
        grid_layout.addWidget(input2, 3, 2, Qt.AlignLeft)

        # Row 4 - Escalation timeout
        grid_layout.addItem(QSpacerItem(125, 0, QSizePolicy.Fixed, QSizePolicy.Minimum), 4, 0)
        input4_label = QLabel("Escalation timeout")
        input4_label.setFixedWidth(120)
        input4_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        input4 = QLineEdit()
        input4.setObjectName("escalation_timeout_input")
        input4.setFixedSize(450, 30)
        input4.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        grid_layout.addWidget(input4_label, 4, 1, Qt.AlignLeft)
        grid_layout.addWidget(input4, 4, 2, Qt.AlignLeft)

        polling_label.mousePressEvent = lambda event: self.toggle_inputs(self.settings_labels, self.settings_inputs)

        self.group_layout.addLayout(grid_layout)

        self.group_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # First row of additional settings layout
        hbox_additional_settings = QHBoxLayout()
        hbox_additional_settings.setAlignment(Qt.AlignLeft)

        additional_label = ClickableLabel("Other Settings")
        additional_label.setObjectName("label_parent")

        additional_label.setFixedWidth(120)
        hbox_additional_settings.addWidget(additional_label)

        must_be_archived_checkbox = QCheckBox("Must Be Archived")
        must_be_archived_checkbox.setObjectName("must_be_archived_checkbox")

        must_be_archived_checkbox.setFixedWidth(200)
        hbox_additional_settings.addWidget(must_be_archived_checkbox)

        target_must_be_archived_checkbox = QCheckBox("Target Must Be Archived")
        target_must_be_archived_checkbox.setObjectName("target_must_be_archived_checkbox")

        target_must_be_archived_checkbox.setFixedWidth(200)
        hbox_additional_settings.addWidget(target_must_be_archived_checkbox)

        rename_with_timestamp_checkbox = QCheckBox("Rename with Timestamp")
        rename_with_timestamp_checkbox.setObjectName("rename_with_timestamp_checkbox")

        hbox_additional_settings.addWidget(rename_with_timestamp_checkbox)

        # Add the first row to the main layout
        self.group_layout.addLayout(hbox_additional_settings)

        # Second row of additional settings layout
        self.group_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        hbox_additional_settings_row_2 = QHBoxLayout()
        hbox_additional_settings_row_2.setAlignment(Qt.AlignLeft)

        # Add spacer to align `History Days` under `Must Be Archived`
        hbox_additional_settings_row_2.addItem(QSpacerItem(120, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))

        # History Days input and label
        history_days_label = QLabel("History Days")
        history_days_label.setFixedWidth(130)
        history_days_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        hbox_additional_settings_row_2.addWidget(history_days_label)
        history_days_input = QLineEdit()
        history_days_input.setObjectName("history_days_input")
        history_days_input.setFixedSize(450, 30)
        hbox_additional_settings_row_2.addWidget(history_days_input)

       # Second row of additional settings layout
        hbox_additional_settings_row_3 = QHBoxLayout()
        hbox_additional_settings_row_3.setAlignment(Qt.AlignLeft)
        hbox_additional_settings_row_3.addItem(QSpacerItem(120, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))

        # Target History Days input and label
        target_history_days_label = QLabel("Target History Days")
        target_history_days_label.setFixedWidth(130)
        target_history_days_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        hbox_additional_settings_row_3.addWidget(target_history_days_label)
        target_history_days_input = QLineEdit()
        target_history_days_input.setObjectName("target_history_days_input")
        target_history_days_input.setFixedSize(450, 30)
        hbox_additional_settings_row_3.addWidget(target_history_days_input)

        # Add the second row to the main layout
        self.group_layout.addLayout(hbox_additional_settings_row_2)
        self.group_layout.addLayout(hbox_additional_settings_row_3)

        # Spacer below the additional settings
        self.group_layout.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))