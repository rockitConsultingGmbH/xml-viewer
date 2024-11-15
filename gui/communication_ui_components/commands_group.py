import logging

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QComboBox, QGroupBox
from PyQt5.QtCore import Qt

from common.connection_manager import ConnectionManager
from common.resource_manager import ResourceManager
from database.utils import delete_from_command, delete_from_commandparam, insert_into_command, insert_into_commandparam, select_from_command, select_from_commandparam, update_commandparam

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

params = {
    "de.bundesbank.acs.filetransfer.post.AcsFiletransferPostCommandSendTksASatz": ["queue1", "queue2"],
    "de.bundesbank.acs.filetransfer.post.AcsFiletransferPostCommandTksSend": ["stage", "anwIdSender", "blzIdSender", "anwIdEmpfaenger", "blzIdEmpfaenger", "dienstId",
                                                                              "format", "satzLaenge", "blockLaenge", "alloc", "compress", "convert", "codepage", "Zahlungsformat", "ExterneReferenz"],
    "de.bundesbank.acs.filetransfer.post.AcsFiletransferPostCommandMQPUT": ["queue", "gFormat", "AnwIdSender", "BlzIdSender", "AnwIdEmpfaenger", "BlzIdEmpfaenger", "DienstId", "GFormat", "GCode",
                                                                           "Dateiformat", "Satzlaenge", "Blocklaenge", "Alloc", "Komprimierung", "Konvertiere", "CodePage", "Zahlungsformat", "DsnMvsInput", "DsnMvsOutput", "ExtReferenz"],
    "de.bundesbank.acs.filetransfer.post.AcsFiletransferPostCommandExecute": ["user", "password", "fingerprints", "soTimeout"],
    "de.bundesbank.acs.filetransfer.post.AcsFiletransferPostCommandChangeDsnOutput": ["rcvaPattern"]
}

class CommandsGroup(QWidget):
    def __init__(self, communication_id=None):
        super().__init__()
        self.communication_id = communication_id
        self.conn_manager = ConnectionManager()
        self.resource_manager = ResourceManager()
        self.vertical_layout = QVBoxLayout()
        self.setLayout(self.vertical_layout)
        self.commands_to_delete = []

    def refresh_commands_ui(self):
        logging.debug("Refreshing commands UI")
        self.commands_to_delete = []
        self.clear_command_fields()
        self.generate_command_ui()

    def create_commands_group(self):
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

        plus_button = QPushButton()
        plus_button.setObjectName("addButton")
        plus_button.setFixedSize(30, 30)
        add_button_icon = self.resource_manager.get_resource_path('gui/icon/plus-button.svg')
        plus_button.setIcon(QIcon(add_button_icon))
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
            self.generate_command_params(selected_classname, 'new')

    def display_fields_for_classname(self, className):
        logging.debug(f"Displaying fields for class: {className}")
        self.clear_command_fields()

        command_group, command_layout = self.generate_command_widget(None, className)
        
        command_label = QLabel(f"<b>New Command: {className.split('.')[-1]}</b>")
        command_label.setAlignment(Qt.AlignLeft)
        command_layout.addWidget(command_label)

        for param_name in params.get(className, []):
            param_input = QLineEdit()
            param_input.setFixedSize(350, 30)
            param_input.setObjectName(f"{param_name}_{className}")

            self.param_widgets[param_name] = param_input
            command_layout.addLayout(self.create_horizontal_layout(param_name, param_input))

        command_group.setLayout(command_layout)
        self.vertical_layout.insertWidget(1, command_group)

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
        for i in reversed(range(self.vertical_layout.count())):
            widget_item = self.vertical_layout.itemAt(i)
            widget = widget_item.widget()
            if widget and isinstance(widget, QGroupBox):
                widget.setParent(None) 
                widget.deleteLater() 

        self.param_widgets.clear()
        self.command_group = None

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
        
        is_new_command = (command_id == 'new')
        command_params = self.get_command_params(command_id) if not is_new_command else {}
        command_params_list = params.get(className, [])
        
        command_label = QLabel(f"<b>{'New Command: ' if is_new_command else ''}{className.split('.')[-1]}</b>")
        command_label.setTextFormat(Qt.RichText)
        command_label.setAlignment(Qt.AlignLeft)

        delete_button = QPushButton()
        delete_button.setObjectName("deleteButton")
        delete_button.setFixedSize(30, 30)
        delete_button_icon = self.resource_manager.get_resource_path('gui/icon/minus-button.svg')
        delete_button.setIcon(QIcon(delete_button_icon))
        delete_button.clicked.connect(lambda: self.delete_command(command_group))
        
        title_layout = QHBoxLayout()
        title_layout.addWidget(command_label)
        title_layout.addWidget(delete_button)
        title_layout.setAlignment(Qt.AlignLeft)
        command_layout.addLayout(title_layout)

        command_layout.addLayout(self.generate_command_classname(className))

        command_type_dropdown = QComboBox()
        command_type_dropdown.addItems(["postCommand", "preCommand"])
        command_type_dropdown.setFixedSize(350, 30)
        command_group.command_type_dropdown = command_type_dropdown

        command_group.param_widgets = {}

        if not is_new_command:
            try:
                conn = self.conn_manager.get_db_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT commandType FROM Command WHERE id = ?", (command_id,))
                result = cursor.fetchone()
                if result and result['commandType'] in ["postCommand", "preCommand"]:
                    command_type_dropdown.setCurrentText(result['commandType'])
            except Exception as e:
                logging.error(f"Failed to fetch command type: {e}")
            finally:
                cursor.close()
                conn.close()

        command_layout.addLayout(self.create_horizontal_layout("Command Type", command_type_dropdown))

        # Conditionally display fields for `de.bundesbank.acs.filetransfer.post.AcsFiletransferPostCommandTksSend`
        if className == "de.bundesbank.acs.filetransfer.post.AcsFiletransferPostCommandTksSend":
            # Retrieve `userid`, `password`, and `validForTargetLocations` if they exist for existing commands
            userid_value = ""
            password_value = ""
            valid_for_target_value = ""
            
            if not is_new_command:
                try:
                    conn = self.conn_manager.get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT userid, password, validForTargetLocations
                        FROM Command
                        WHERE id = ?
                    """, (command_id,))
                    result = cursor.fetchone()
                    if result:
                        userid_value = result['userid'] or ""
                        password_value = result['password'] or ""
                        valid_for_target_value = result['validForTargetLocations'] or ""
                except Exception as e:
                    logging.error(f"Failed to fetch additional fields for command: {e}")
                finally:
                    cursor.close()
                    conn.close()

            userid_field = QLineEdit(userid_value)
            password_field = QLineEdit(password_value)
            valid_for_target_field = QLineEdit(valid_for_target_value)

            command_group.userid_field = userid_field
            command_group.password_field = password_field
            command_group.valid_for_target_field = valid_for_target_field

            command_layout.addLayout(self.create_horizontal_layout("userid", userid_field))
            command_layout.addLayout(self.create_horizontal_layout("password", password_field))
            command_layout.addLayout(self.create_horizontal_layout("validForTargetLocations", valid_for_target_field))

        # Create input fields for each parameter and add to the command_group's param_widgets
        for param_name in command_params_list:
            param_value = command_params.get(param_name, '') if not is_new_command else ''
            param_input = QLineEdit(param_value)
            command_group.param_widgets[param_name] = param_input
            command_layout.addLayout(self.create_horizontal_layout(param_name, param_input))

        command_group.setLayout(command_layout)
        self.vertical_layout.insertWidget(1, command_group)

    def delete_command(self, command_widget):
        command_id = getattr(command_widget, "command_id", None)
        
        if command_id and command_id != 'new':
            if command_id not in self.commands_to_delete:
                self.commands_to_delete.append(command_id)
                logging.info(f"Marked command ID: {command_id} for deletion")

        command_widget.setParent(None)
        command_widget.deleteLater()

    def save_commands(self):
        logging.info("Saving commands to database")
        try:
            conn = self.conn_manager.get_db_connection()
            cursor = conn.cursor()

            for command_id in self.commands_to_delete:
                try:
                    delete_from_commandparam(cursor, command_id)
                    delete_from_command(cursor, command_id)
                    logging.info(f"Deleted command ID: {command_id} from the database")
                except Exception as e:
                    logging.error(f"Failed to delete command ID: {command_id} - {e}")

            for command_widget in self.findChildren(QGroupBox):
                command_id = getattr(command_widget, "command_id", None)
                class_name = command_widget.objectName()
                
                if command_id in self.commands_to_delete:
                    continue

                command_type_dropdown = getattr(command_widget, "command_type_dropdown", None)
                command_type = command_type_dropdown.currentText() if command_type_dropdown else "postCommand"
                
                if command_id and command_id != 'new':
                    self.update_command(cursor, command_id, class_name, command_type, command_widget)
                else:
                    command_id = self.insert_command(cursor, command_id, class_name, command_type, command_widget)

                if class_name == "de.bundesbank.acs.filetransfer.post.AcsFiletransferPostCommandTksSend" and command_id:
                    userid_field = getattr(command_widget, "userid_field", None)
                    password_field = getattr(command_widget, "password_field", None)
                    valid_for_target_field = getattr(command_widget, "valid_for_target_field", None)

                    cursor.execute("""
                        UPDATE Command 
                        SET userid = ?, password = ?, validForTargetLocations = ?, commandType = ?
                        WHERE id = ?
                    """, (
                        userid_field.text() if userid_field else "",
                        password_field.text() if password_field else "",
                        valid_for_target_field.text() if valid_for_target_field else "",
                        command_type,
                        command_id
                    ))

            conn.commit()
            logging.info("Commands and parameters saved successfully")
            
            self.commands_to_delete.clear()
            self.refresh_commands_ui()

        except Exception as e:
            conn.rollback()
            logging.error(f"Failed to save commands: {e}")
        finally:
            cursor.close()
            conn.close()

    def insert_command(self, cursor, command_id, class_name, command_type, command_widget):
        logging.debug(f"Inserting new command for class: {class_name}")

        # Handle additional fields for `AcsFiletransferPostCommandTksSend`
        userid = getattr(command_widget, "userid_field", QLineEdit("")).text()
        password = getattr(command_widget, "password_field", QLineEdit("")).text()
        valid_for_target_locations = getattr(command_widget, "valid_for_target_field", QLineEdit("")).text()

        row = {
            "communication_id": self.communication_id,
            "className": class_name,
            "commandType": command_type,
            "userid": userid,
            "password": password,
            "validForTargetLocations": valid_for_target_locations
        }
        insert_into_command(cursor, row)
        command_id = cursor.lastrowid
        logging.debug(f"New command ID: {command_id}")

        for order, (param_name, param_widget) in enumerate(command_widget.param_widgets.items(), start=1):
            param_value = param_widget.text()
            logging.debug(f"Inserting parameter - Name: {param_name}, Value: {param_value}, Order: {order}")
            row = {
                "command_id": command_id,
                "param": param_value,
                "paramName": param_name,
                "paramOrder": order
            }
            insert_into_commandparam(cursor, row)
        
        return command_id

    def update_command(self, cursor, command_id, class_name, command_type, command_widget):
        logging.debug(f"Updating command ID: {command_id}, class: {class_name}")

        # Access the additional fields if the command class requires it
        if class_name == "de.bundesbank.acs.filetransfer.post.AcsFiletransferPostCommandTksSend":
            userid = getattr(command_widget, "userid_field", QLineEdit("")).text()
            password = getattr(command_widget, "password_field", QLineEdit("")).text()
            valid_for_target_locations = getattr(command_widget, "valid_for_target_field", QLineEdit("")).text()
            
            cursor.execute("""
                UPDATE Command 
                SET commandType = ?, userid = ?, password = ?, validForTargetLocations = ?
                WHERE id = ?
                """, (
                command_type,
                userid,
                password,
                valid_for_target_locations,
                command_id
            ))
        else:
            cursor.execute("""
                UPDATE Command 
                SET commandType = ?
                WHERE id = ?
            """, (
                command_type,
                command_id
            ))

        for param_name, param_widget in command_widget.param_widgets.items():
            param_value = param_widget.text()
            logging.debug(f"Updating parameter - Name: {param_name}, Value: {param_value}")

            row = {
                "command_id": command_id,
                "param": param_value,
                "paramName": param_name
            }
            update_commandparam(cursor, row)

    def set_fields_from_db(self):
        logging.info("Resetting fields to original state from the database")
        self.refresh_commands_ui()
