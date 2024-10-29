from PyQt5.QtWidgets import QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from common.connection_manager import ConnectionManager
from database.utils import select_from_command, select_from_commandparam

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
            rows = select_from_command(cursor, self.communication_id).fetchall()
            for row in rows:
                command_id = row['id']
                class_name = row['className']
                if class_name:
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
        bold_font = QFont()
        bold_font.setBold(True)
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

