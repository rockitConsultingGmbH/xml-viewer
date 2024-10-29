from PyQt5.QtWidgets import QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from common.connection_manager import ConnectionManager
from database.utils import select_from_command, select_from_commandparam

class CommandFactory:
    @staticmethod
    def create_command_ui(commands_ui, className, command_id):
        if className == "de.bundesbank.acs.filetransfer.post.AcsFiletransferPostCommandSendTksASatz":
            commands_ui.generate_send_tks_a_satz(className, command_id)
        elif className == "de.bundesbank.acs.filetransfer.post.AcsFiletransferPostCommandTksSend":
            commands_ui.generate_tks_send(className, command_id)
        elif className == "de.bundesbank.acs.filetransfer.post.AcsFiletransferPostCommandMQPUT":
            commands_ui.generate_mq_put(className, command_id)
        elif className == "de.bundesbank.acs.filetransfer.post.AcsFiletransferPostCommandExecute":
            commands_ui.generate_execute(className, command_id)
        elif className == "de.bundesbank.acs.filetransfer.post.AcsFiletransferPostCommandChangeDsnOutput":
            commands_ui.generate_change_dsn_output()
        else:
            raise ValueError(f"Unknown class name: {className}")

class CommandsUI(QWidget):
    def __init__(self, communication_id = None):
        super().__init__()
        self.communication_id = communication_id
        self.conn_manager = ConnectionManager()
        self.vertical_layout = QVBoxLayout()
        self.init_commands_ui()

    def init_commands_ui(self):
        self.setLayout(self.vertical_layout)

    def create_horizontal_layout(self, label_text, input_field, is_classname=False):
        label = QLabel(label_text)
        label.setFixedWidth(120)

        if is_classname:
            input_field.setFixedSize(550, 30)
        else:
            input_field.setFixedSize(350, 30)

        h_layout = QHBoxLayout()
        h_layout.addWidget(label)
        h_layout.addWidget(input_field)
        h_layout.setAlignment(Qt.AlignLeft)
        return h_layout
    
    def generate_command_ui(self):
        try:
            conn = self.conn_manager.get_db_connection()
            cursor = conn.cursor()
            # Dummy rows for testing
            #rows = [
            #    {'className': 'de.bundesbank.acs.filetransfer.post.AcsFiletransferPostCommandSendTksASatz'},
            #    {'className': 'de.bundesbank.acs.filetransfer.post.AcsFiletransferPostCommandTksSend'},
                #{'className': 'de.bundesbank.acs.filetransfer.post.AcsFiletransferPostCommandMQPUT'},
                #{'className': 'de.bundesbank.acs.filetransfer.post.AcsFiletransferPostCommandExecute'},
                #{'className': 'de.bundesbank.acs.filetransfer.post.AcsFiletransferPostCommandChangeDsnOutput'}
            #]
            rows = select_from_command(cursor, self.communication_id).fetchall()
            print(rows)
            for row in rows:
                command_id = row['id']
                class_name = row['className']
                print(f"Class name: {class_name} - Command ID: {command_id}")
                if class_name:
                    #CommandFactory.create_command_ui(self, class_name, command_id)
                    self.generate_command_params(class_name, command_id)
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cursor.close()
            conn.close()

    def get_command_params(self, command_id):
        try:
            conn = self.conn_manager.get_db_connection()
            cursor = conn.cursor()
            rows = select_from_commandparam(cursor, command_id).fetchall()
            return rows
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cursor.close()
            conn.close()

    def generate_command_classname(self, className):
        command_classname_input = QLineEdit(className)
        #command_classname_input = QLabel(className)
        bold_font = QFont()
        bold_font.setBold(True)
        #command_classname_input.setFont(bold_font)
        command_classname_input.setObjectName("command_classname")

        h_layout = self.create_horizontal_layout("Classname", command_classname_input, is_classname=True)
        return h_layout

    def generate_command_widget(self, command_id):
        command_widget = QWidget()
        command_widget.setObjectName(f"command_widget_{command_id}")
        command_widget.setProperty("command_widget_id", command_id)
        command_box = QVBoxLayout(command_widget)
        command_box.setObjectName(f"command_box_{command_id}")
        return command_widget, command_box
    
    def generate_command_params_dict(self, command_id):
        command_params = self.get_command_params(command_id)
        params_dict = {param['paramName']: param['param'] for param in command_params}
        return params_dict

    def generate_command_params(self, className, command_id):
        command_widget, command_box = self.generate_command_widget(command_id)
        command_params = self.get_command_params(command_id)
        
        # Add a label for the whole box
        box_label = QLabel(className.split('.')[-1])
        box_label.setAlignment(Qt.AlignLeft)
        box_label.setStyleSheet("font-weight: bold; font-style: italic;")
        command_box.addWidget(box_label)
        command_box.addLayout(self.generate_command_classname(className))

        param_widgets = {}
        for param in command_params:
            param_name = param['paramName']
            param_input = QLineEdit(param['param'])
            param_input.setObjectName(f"{param_name}_{command_id}")
            param_widgets[param_name] = param_input
            command_box.addLayout(self.create_horizontal_layout(param_name, param_input))
        self.vertical_layout.addWidget(command_widget)

    def generate_send_tks_a_satz(self, className, command_id):
        command_widget, command_box = self.generate_command_widget(command_id)
        command_params = self.get_command_params(command_id)
        
        # Add a label for the whole box
        box_label = QLabel("SendTksASatz Command")
        box_label.setAlignment(Qt.AlignLeft)
        box_label.setStyleSheet("font-weight: bold; font-style: italic;")
        command_box.addWidget(box_label)
        command_box.addLayout(self.generate_command_classname(className))

        # Set a border for the command box
        #command_widget.setStyleSheet("border: 1px solid black; padding: 10px;")
    
        send_tks_a_satz_queue_input = QLineEdit()
        send_tks_a_satz_queue_input.setObjectName("send_tks_a_satz_queue")
        command_box.addLayout(self.create_horizontal_layout("Queue", send_tks_a_satz_queue_input))

        self.vertical_layout.addWidget(command_widget)

    def generate_tks_send(self, className, command_id):
        command_widget, command_box = self.generate_command_widget(command_id)
        command_params = self.get_command_params(command_id)
        
        # Add a label for the whole box
        box_label = QLabel("TksSend Command")
        box_label.setAlignment(Qt.AlignLeft)
        box_label.setStyleSheet("font-weight: bold; font-style: italic;")
        command_box.addWidget(box_label)
        command_box.addLayout(self.generate_command_classname(className))

        param_widgets = {}
        for param in command_params:
            param_name = param['paramName']
            param_input = QLineEdit(param['param'])
            param_input.setObjectName(f"{param_name}_{command_id}")
            param_widgets[param_name] = param_input
            command_box.addLayout(self.create_horizontal_layout(param_name, param_input))
        self.vertical_layout.addWidget(command_widget)

    def generate_mq_put(self, className, command_id):
        command_widget, command_box = self.generate_command_widget(command_id)
        command_params = self.get_command_params(command_id)
        
        # Add a label for the whole box
        box_label = QLabel("MQPUT Command")
        box_label.setAlignment(Qt.AlignLeft)
        box_label.setStyleSheet("font-weight: bold; font-style: italic;")
        command_box.addWidget(box_label)
        command_box.addLayout(self.generate_command_classname(className))

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

        command_box.addLayout(self.create_horizontal_layout("Queue", mq_put_queue_input))
        command_box.addLayout(self.create_horizontal_layout("GFormat", mq_put_g_format_input))
        command_box.addLayout(self.create_horizontal_layout("AnwIdSender", mq_put_anw_id_sender_input))
        command_box.addLayout(self.create_horizontal_layout("BlzIdSender", mq_put_blz_id_sender_input))
        command_box.addLayout(self.create_horizontal_layout("AnwIdEmpfaenger", mq_put_anw_id_empfaenger_input))
        command_box.addLayout(self.create_horizontal_layout("BlzIdEmpfaenger", mq_put_blz_id_empfaenger_input))
        command_box.addLayout(self.create_horizontal_layout("DienstId", mq_put_dienst_id_input))
        command_box.addLayout(self.create_horizontal_layout("ExtReferenz", mq_put_ext_referenz_input))
        command_box.addLayout(self.create_horizontal_layout("DsnMvsOutput", mq_put_dsn_mvs_output_input))
    
        self.vertical_layout.addWidget(command_widget)

    def generate_execute(self, className, command_id):
        command_widget, command_box = self.generate_command_widget(command_id)
        command_params = self.get_command_params(command_id)
        
        # Add a label for the whole box
        box_label = QLabel("Execute Command")
        box_label.setAlignment(Qt.AlignLeft)
        box_label.setStyleSheet("font-weight: bold; font-style: italic;")
        command_box.addWidget(box_label)
        command_box.addLayout(self.generate_command_classname(className))

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

        command_box.addLayout(self.create_horizontal_layout("Servername", execute_servername_input))
        command_box.addLayout(self.create_horizontal_layout("Username", execute_username_input))
        command_box.addLayout(self.create_horizontal_layout("Password", execute_password_input))
        command_box.addLayout(self.create_horizontal_layout("Fingerprints", execute_fingerprints_input))
        command_box.addLayout(self.create_horizontal_layout("SoTimeout", execute_so_timeout_input))

        self.vertical_layout.addWidget(command_widget)

    def generate_change_dsn_output(self, className, command_id):
        command_widget, command_box = self.generate_command_widget(command_id)
        command_params = self.get_command_params(command_id)
        
        # Add a label for the whole box
        box_label = QLabel("ChangeDsnOutput Command")
        box_label.setAlignment(Qt.AlignLeft)
        box_label.setStyleSheet("font-weight: bold; font-style: italic;")
        command_box.addWidget(box_label)
        command_box.addLayout(self.generate_command_classname(className))

        dsn_output_rcva_pattern_input = QLineEdit()
        dsn_output_rcva_pattern_input.setObjectName("dsn_output_rcva_pattern")
        command_box.addLayout(self.create_horizontal_layout("rcvaPattern", dsn_output_rcva_pattern_input))

        self.vertical_layout.addWidget(command_widget)
