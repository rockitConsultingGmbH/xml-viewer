from PyQt5.QtWidgets import QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt


class CommandsUI(QWidget):
    def __init__(self):
        super().__init__()
        self.vertical_layout = QVBoxLayout()
        self.init_commands_ui()

    def init_commands_ui(self):
        self.setLayout(self.vertical_layout)

    def create_horizontal_layout(self, label_text, input_field, is_classname=False):
        label = QLabel(label_text)
        label.setFixedWidth(120)

        if is_classname:
            input_field.setFixedHeight(30)
        else:
            input_field.setFixedSize(550, 30)

        h_layout = QHBoxLayout()
        h_layout.addWidget(label)
        h_layout.addWidget(input_field)
        h_layout.setAlignment(Qt.AlignLeft)
        return h_layout

    def generate_postcommand_classname(self):
        postcommand_classname_input = QLineEdit()
        postcommand_classname_input.setObjectName("postcommand_classname")

        h_layout = self.create_horizontal_layout("Classname", postcommand_classname_input, is_classname=True)
        return h_layout

    def generate_send_tks_a_satz(self):
        self.vertical_layout.addLayout(self.generate_postcommand_classname())

        send_tks_a_satz_queue_input = QLineEdit()
        send_tks_a_satz_queue_input.setObjectName("send_tks_a_satz_queue")

        h_layout = self.create_horizontal_layout("Queue", send_tks_a_satz_queue_input)
        self.vertical_layout.addLayout(h_layout)

    def generate_tks_send(self):
        self.vertical_layout.addLayout(self.generate_postcommand_classname())

        tks_send_stage_input = QLineEdit()
        tks_send_stage_input.setObjectName("tks_send_stage")

        tks_send_anw_id_sender_input = QLineEdit()
        tks_send_anw_id_sender_input.setObjectName("tks_send_anw_id_sender")
        tks_send_blz_id_sender_input = QLineEdit()
        tks_send_blz_id_sender_input.setObjectName("tks_send_blz_id_sender")
        tks_send_anw_id_empfaenger_input = QLineEdit()
        tks_send_anw_id_empfaenger_input.setObjectName("tks_send_anw_id_empfaenger")
        tks_send_blz_id_empfaenger_input = QLineEdit()
        tks_send_blz_id_empfaenger_input.setObjectName("tks_send_blz_id_empfaenger")
        tks_send_dienst_id_input = QLineEdit()
        tks_send_dienst_id_input.setObjectName("tks_send_dienst_id")
        tks_send_format_input = QLineEdit()
        tks_send_format_input.setObjectName("tks_send_format")
        tks_send_satz_laenge_input = QLineEdit()
        tks_send_satz_laenge_input.setObjectName("tks_send_satz_laenge")
        tks_send_block_laenge_input = QLineEdit()
        tks_send_block_laenge_input.setObjectName("tks_send_block_laenge")
        tks_send_alloc_input = QLineEdit()
        tks_send_alloc_input.setObjectName("tks_send_alloc")
        tks_send_compress_input = QLineEdit()
        tks_send_compress_input.setObjectName("tks_send_compress")
        tks_send_convert_input = QLineEdit()
        tks_send_convert_input.setObjectName("tks_send_convert")
        tks_send_codepage_input = QLineEdit()
        tks_send_codepage_input.setObjectName("tks_send_codepage")
        tks_send_zahlungsformat_input = QLineEdit()
        tks_send_zahlungsformat_input.setObjectName("tks_send_zahlungsformat")
        tks_send_externe_referenz_input = QLineEdit()
        tks_send_externe_referenz_input.setObjectName("tks_send_externe_referenz")

        self.vertical_layout.addLayout(self.create_horizontal_layout("Stage", tks_send_stage_input))
        self.vertical_layout.addLayout(self.create_horizontal_layout("AnwIdSender", tks_send_anw_id_sender_input))
        self.vertical_layout.addLayout(self.create_horizontal_layout("BlzIdSender", tks_send_blz_id_sender_input))
        self.vertical_layout.addLayout(self.create_horizontal_layout("AnwIdEmpfaenger", tks_send_anw_id_empfaenger_input))
        self.vertical_layout.addLayout(self.create_horizontal_layout("BlzIdEmpfaenger", tks_send_blz_id_empfaenger_input))
        self.vertical_layout.addLayout(self.create_horizontal_layout("DienstId", tks_send_dienst_id_input))
        self.vertical_layout.addLayout(self.create_horizontal_layout("Format", tks_send_format_input))
        self.vertical_layout.addLayout(self.create_horizontal_layout("SatzLaenge", tks_send_satz_laenge_input))
        self.vertical_layout.addLayout(self.create_horizontal_layout("BlockLaenge", tks_send_block_laenge_input))
        self.vertical_layout.addLayout(self.create_horizontal_layout("Alloc", tks_send_alloc_input))
        self.vertical_layout.addLayout(self.create_horizontal_layout("Compress", tks_send_compress_input))
        self.vertical_layout.addLayout(self.create_horizontal_layout("Convert", tks_send_convert_input))
        self.vertical_layout.addLayout(self.create_horizontal_layout("Codepage", tks_send_codepage_input))
        self.vertical_layout.addLayout(self.create_horizontal_layout("Zahlungsformat", tks_send_zahlungsformat_input))
        self.vertical_layout.addLayout(self.create_horizontal_layout("ExterneReferenz", tks_send_externe_referenz_input))

    def generate_mq_put(self):
        self.vertical_layout.addLayout(self.generate_postcommand_classname())

        mq_put_queue_input = QLineEdit()
        mq_put_queue_input.setObjectName("mq_put_queue")

        mq_put_g_format_input = QLineEdit()
        mq_put_g_format_input.setObjectName("mq_put_g_format")
        mq_put_anw_id_sender_input = QLineEdit()
        mq_put_anw_id_sender_input.setObjectName("mq_put_anw_id_sender")
        mq_put_blz_id_sender_input = QLineEdit()
        mq_put_blz_id_sender_input.setObjectName("mq_put_blz_id_sender")
        mq_put_anw_id_empfaenger_input = QLineEdit()
        mq_put_anw_id_empfaenger_input.setObjectName("mq_put_anw_id_empfaenger")
        mq_put_blz_id_empfaenger_input = QLineEdit()
        mq_put_blz_id_empfaenger_input.setObjectName("mq_put_blz_id_empfaenger")
        mq_put_dienst_id_input = QLineEdit()
        mq_put_dienst_id_input.setObjectName("mq_put_dienst_id")
        mq_put_ext_referenz_input = QLineEdit()
        mq_put_ext_referenz_input.setObjectName("mq_put_ext_referenz")
        mq_put_dsn_mvs_output_input = QLineEdit()
        mq_put_dsn_mvs_output_input.setObjectName("mq_put_dsn_mvs_output")

        self.vertical_layout.addLayout(self.create_horizontal_layout("Queue", mq_put_queue_input))
        self.vertical_layout.addLayout(self.create_horizontal_layout("GFormat", mq_put_g_format_input))
        self.vertical_layout.addLayout(self.create_horizontal_layout("AnwIdSender", mq_put_anw_id_sender_input))
        self.vertical_layout.addLayout(self.create_horizontal_layout("BlzIdSender", mq_put_blz_id_sender_input))
        self.vertical_layout.addLayout(self.create_horizontal_layout("AnwIdEmpfaenger", mq_put_anw_id_empfaenger_input))
        self.vertical_layout.addLayout(self.create_horizontal_layout("BlzIdEmpfaenger", mq_put_blz_id_empfaenger_input))
        self.vertical_layout.addLayout(self.create_horizontal_layout("DienstId", mq_put_dienst_id_input))
        self.vertical_layout.addLayout(self.create_horizontal_layout("ExtReferenz", mq_put_ext_referenz_input))
        self.vertical_layout.addLayout(self.create_horizontal_layout("DsnMvsOutput", mq_put_dsn_mvs_output_input))

    def generate_execute(self):
        self.vertical_layout.addLayout(self.generate_postcommand_classname())

        execute_servername_input = QLineEdit()
        execute_servername_input.setObjectName("execute_servername")

        execute_username_input = QLineEdit()
        execute_username_input.setObjectName("execute_username")
        execute_password_input = QLineEdit()
        execute_password_input.setObjectName("execute_password")
        execute_fingerprints_input = QLineEdit()
        execute_fingerprints_input.setObjectName("execute_fingerprints")
        execute_so_timeout_input = QLineEdit()
        execute_so_timeout_input.setObjectName("execute_so_timeout")

        self.vertical_layout.addLayout(self.create_horizontal_layout("Servername", execute_servername_input))
        self.vertical_layout.addLayout(self.create_horizontal_layout("Username", execute_username_input))
        self.vertical_layout.addLayout(self.create_horizontal_layout("Password", execute_password_input))
        self.vertical_layout.addLayout(self.create_horizontal_layout("Fingerprints", execute_fingerprints_input))
        self.vertical_layout.addLayout(self.create_horizontal_layout("SoTimeout", execute_so_timeout_input))

    def generate_change_dsn_output(self):
        self.vertical_layout.addLayout(self.generate_postcommand_classname())

        dsn_output_rcva_pattern_input = QLineEdit()
        dsn_output_rcva_pattern_input.setObjectName("dsn_output_rcva_pattern")

        self.vertical_layout.addLayout(self.create_horizontal_layout("RcvaPattern", dsn_output_rcva_pattern_input))
