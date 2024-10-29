import logging
from PyQt5.QtWidgets import QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QComboBox, QGroupBox
from PyQt5.QtCore import Qt

from common.connection_manager import ConnectionManager
from database.utils import select_from_command, select_from_commandparam

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

params = {
    "de.bundesbank.acs.filetransfer.post.AcsFiletransferPostCommandSendTksASatz": ["queue", "queue"],
    "de.bundesbank.acs.filetransfer.post.AcsFiletransferPostCommandTksSend": ["stage", "anwIdSender", "blzIdSender", "anwIdEmpfaenger", "blzIdEmpfaenger", "dienstId",
                                                                              "format", "satzLaenge", "blockLaenge", "alloc", "compress", "convert", "codepage", "Zahlungsformat", "ExterneReferenz"],
    "de.bundesbank.acs.filetransfer.post.AcsFiletransferPostCommandMQPUT": ["queue", "gFormat", "AnwIdSender", "BlzIdSender", "AnwIdEmpfaenger", "BlzIdEmpfaenger", "DienstId", "GFormat", "GCode",
                                                                           "Dateiformat", "Satzlaenge", "Blocklaenge", "Alloc", "Komprimierung", "Konvertiere", "CodePage", "Zahlungsformat", "DsnMvsInput", "DsnMvsOutput", "ExtReferenz"],
    "de.bundesbank.acs.filetransfer.post.AcsFiletransferPostCommandExecute": ["user", "password", "fingerprints", "soTimeout"],
    "de.bundesbank.acs.filetransfer.post.AcsFiletransferPostCommandChangeDsnOutput": ["rcvaPattern"]
}

class CommandsUI(QWidget):
    def __init__(self, communication_id=None):
        super().__init__()
        self.communication_id = communication_id
        self.conn_manager = ConnectionManager()
        self.vertical_layout = QVBoxLayout()
        self.setLayout(self.vertical_layout)

        #self.init_commands_ui()

    def init_commands_ui(self):
        logging.debug("Initializing commands UI")
        self.dropdown = QComboBox()
        self.param_widgets = {}
        self.command_group = None

        self.add_new_command_controls()
        self.generate_command_ui()

    def add_new_command_controls(self):
        logging.debug("Adding new command controls")
        self.dropdown.addItems(params.keys())
        self.dropdown.setFixedSize(550, 30)

        plus_button = QPushButton("+")
        plus_button.setFixedSize(20, 20)
        plus_button.clicked.connect(self.add_new_command)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.dropdown)
        button_layout.addWidget(plus_button)
        button_layout.setAlignment(Qt.AlignLeft)

        self.vertical_layout.insertLayout(0, button_layout)

    def add_new_command(self):
        selected_classname = self.dropdown.currentText()
        logging.debug(f"Adding new command: {selected_classname}")
        if selected_classname:
            self.display_fields_for_classname(selected_classname)

    def display_fields_for_classname(self, className):
        logging.debug(f"Displaying fields for class: {className}")
        self.clear_command_fields()

        self.command_group = QGroupBox()
        command_layout = QVBoxLayout()
        
        command_label = QLabel(f"<b>New Command: {className.split('.')[-1]}</b>")
        command_label.setAlignment(Qt.AlignLeft)
        command_layout.addWidget(command_label)

        for param_name in params.get(className, []):
            param_input = QLineEdit()
            param_input.setFixedSize(350, 30)
            param_input.setObjectName(f"{param_name}_{className}")

            self.param_widgets[param_name] = param_input
            command_layout.addLayout(self.create_horizontal_layout(param_name, param_input))

        self.command_group.setLayout(command_layout)
        self.vertical_layout.insertWidget(1, self.command_group)

    def create_horizontal_layout(self, label_text, input_field, is_classname=False):
        label = QLabel(label_text)
        label.setFixedWidth(120)
        input_field.setFixedSize(350, 30) if not is_classname else input_field.setFixedSize(550, 30)

        h_layout = QHBoxLayout()
        h_layout.addWidget(label)
        h_layout.addWidget(input_field)
        h_layout.setAlignment(Qt.AlignLeft)
        return h_layout

    def clear_command_fields(self):
        logging.debug("Clearing command fields")
        if self.command_group:
            self.command_group.setParent(None)
            self.command_group.deleteLater()
            self.command_group = None
        self.param_widgets.clear()

    def generate_command_ui(self):
        logging.debug("Generating command UI from database")
        try:
            conn = self.conn_manager.get_db_connection()
            cursor = conn.cursor()
            rows = select_from_command(cursor, self.communication_id).fetchall()
            for row in rows:
                command_id = row['id']
                class_name = row['className']
                if class_name:
                    self.generate_command_params(class_name, command_id)
        except Exception as e:
            logging.error(f"Error generating command UI: {e}")
        finally:
            cursor.close()
            conn.close()

    def get_command_params(self, command_id):
        logging.debug(f"Fetching command parameters for command ID: {command_id}")
        try:
            conn = self.conn_manager.get_db_connection()
            cursor = conn.cursor()
            rows = select_from_commandparam(cursor, command_id).fetchall()
            return {param['paramName']: param['param'] for param in rows}
        
        except Exception as e:
            logging.error(f"Error fetching command parameters: {e}")
            return {}
        finally:
            cursor.close()
            conn.close()

    def generate_command_classname(self, className):
        command_classname_input = QLineEdit(className)
        command_classname_input.setReadOnly(True)
        h_layout = self.create_horizontal_layout("Classname", command_classname_input, is_classname=True)
        return h_layout

    def generate_command_widget(self, command_id, className=None):
        command_group = QGroupBox()
        command_group.command_id = command_id
        command_layout = QVBoxLayout()
        command_group.setObjectName(className)
        return command_group, command_layout

    def generate_command_params(self, className, command_id):
        logging.debug(f"Generating command parameters for class: {className}, command ID: {command_id}")
        command_group, command_layout = self.generate_command_widget(command_id, className)
        
        command_params = self.get_command_params(command_id)
        command_params_list = params.get(className, [])

        command_label = QLabel(f"<b>{className.split('.')[-1]}</b>")
        command_label.setTextFormat(Qt.RichText)
        command_label.setAlignment(Qt.AlignLeft)
        command_layout.addWidget(command_label)

        #command_classname_input = QLineEdit(className)
        #command_classname_input.setReadOnly(True)
        #command_layout.addWidget(command_classname_input)
        command_layout.addLayout(self.generate_command_classname(className))

        for param_name in command_params_list:
            param_value = command_params.get(param_name, '')
            param_input = QLineEdit(param_value)
            param_input.setObjectName(f"{param_name}_{command_id}")    ## SET HERE
            command_layout.addLayout(self.create_horizontal_layout(param_name, param_input))
        
        command_group.setLayout(command_layout)
        self.vertical_layout.addWidget(command_group)

    def save_commands(self):
        logging.info("Saving commands to database")
        try:
            conn = self.conn_manager.get_db_connection()
            cursor = conn.cursor()

            for command_widget in self.findChildren(QGroupBox):
                print("Command widget:", command_widget)
                if isinstance(command_widget, QGroupBox):
                    command_id = getattr(command_widget, "command_id", None)
                    class_name = command_widget.objectName()
                    print("Command ID:", command_id, "Class Name:", class_name)
                    
                    if command_id:
                        self.update_command(cursor, command_id, class_name, command_widget)
                    else:
                        self.insert_command(cursor, class_name, command_widget)

            conn.commit()
            logging.info("Commands and parameters saved successfully")
        except Exception as e:
            conn.rollback()
            logging.error(f"Failed to save commands: {e}")
        finally:
            cursor.close()
            conn.close()

    def update_command(self, cursor, command_id, class_name, command_widget):
        logging.debug(f"Updating command ID: {command_id}, class: {class_name}")
        for param_name in params.get(class_name, []):
            param_widget = command_widget.findChild(QLineEdit, f"{param_name}_{command_id}")   ## SET HERE
            if param_widget:
                param_value = param_widget.text()
                logging.debug(f"Param Name: {param_name}, Param Value: {param_value}")
                cursor.execute("""
                UPDATE CommandParam
                SET param = ?
                WHERE command_id = ? and paramName = ?
                """, (
                    param_value,
                    command_id,
                    param_name
                ))

    def insert_command(self, cursor, class_name, command_widget):
        logging.debug(f"Inserting new command for class: {class_name}")
        for param_name in params.get(class_name, []):
            param_widget = command_widget.findChild(QLineEdit, f"{param_name}_{command_id}")   ## SET HERE
            if param_widget:
                param_value = param_widget.text()
                logging.debug(f"Param Name: {param_name}, Param Value: {param_value}")
                cursor.execute("""
                    INSERT INTO Command (communication_id, className, commandType)
                    VALUES (?, ?, ?)
                """, (self.communication_id, class_name, 'postCommand'))
                
                command_id = cursor.lastrowid

        for order, param_name in enumerate(params.get(class_name, []), start=1):
            param_value = self.param_widgets[param_name].text()
            cursor.execute("""
                INSERT INTO CommandParam (command_id, param, paramName, paramOrder)
                VALUES (?, ?, ?, ?)
            """, (command_id, param_value, param_name, order))
