import logging
from PyQt5.QtWidgets import QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QComboBox, QGroupBox
from PyQt5.QtCore import Qt

from common.connection_manager import ConnectionManager
from database.utils import select_from_command, select_from_commandparam

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
        self.vertical_layout = QVBoxLayout()
        self.setLayout(self.vertical_layout)

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

        plus_button = QPushButton("+")
        plus_button.setFixedSize(30, 30)
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

    def delete_command(self, command_widget):
        command_id = getattr(command_widget, "command_id", None)
        
        if command_id and command_id != 'new':
            try:
                conn = self.conn_manager.get_db_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM CommandParam WHERE command_id = ?", (command_id,))
                cursor.execute("DELETE FROM Command WHERE id = ?", (command_id,))
                
                conn.commit()
                logging.info(f"Deleted command ID: {command_id} from the database")

            except Exception as e:
                conn.rollback()
                logging.error(f"Failed to delete command ID: {command_id} - {e}")
            finally:
                cursor.close()
                conn.close()

        command_widget.setParent(None)
        command_widget.deleteLater()

    def generate_command_params(self, className, command_id):
        logging.debug(f"Generating command parameters for class: {className}, command ID: {command_id}")

        # Create a group for the command with layout
        command_group, command_layout = self.generate_command_widget(command_id, className)
        
        # Check if this is a new command
        is_new_command = (command_id == 'new')
        command_params = self.get_command_params(command_id) if not is_new_command else {}
        command_params_list = params.get(className, [])
        
        # Command label at the top
        command_label = QLabel(f"<b>{'New Command: ' if is_new_command else ''}{className.split('.')[-1]}</b>")
        command_label.setTextFormat(Qt.RichText)
        command_label.setAlignment(Qt.AlignLeft)

        # Horizontal layout for the command title and delete button
        delete_button = QPushButton("-")
        delete_button.setFixedSize(30, 30)
        delete_button.clicked.connect(lambda: self.delete_command(command_group))
        
        title_layout = QHBoxLayout()
        title_layout.addWidget(command_label)
        title_layout.addWidget(delete_button)
        title_layout.setAlignment(Qt.AlignLeft)
        command_layout.addLayout(title_layout)

        # Add classname as a read-only input field below the label
        command_layout.addLayout(self.generate_command_classname(className))

        # Add a dropdown to select `commandType` (for both new and existing commands)
        self.command_type_dropdown = QComboBox()
        self.command_type_dropdown.addItems(["postCommand", "preCommand"])
        self.command_type_dropdown.setFixedSize(350, 30)

        # Set current value for existing commands
        if not is_new_command:
            try:
                conn = self.conn_manager.get_db_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT commandType FROM Command WHERE id = ?", (command_id,))
                result = cursor.fetchone()
                if result and result['commandType'] in ["postCommand", "preCommand"]:
                    self.command_type_dropdown.setCurrentText(result['commandType'])
            except Exception as e:
                logging.error(f"Failed to fetch command type: {e}")
            finally:
                cursor.close()
                conn.close()

        command_layout.addLayout(self.create_horizontal_layout("Command Type", self.command_type_dropdown))

        # Display `userID`, `password`, and `validForTargetLocations` fields only if the class is `AcsFiletransferPostCommandTksSend`
        if className == "de.bundesbank.acs.filetransfer.post.AcsFiletransferPostCommandTksSend":
            self.userid_field = QLineEdit("")
            self.password_field = QLineEdit("")
            self.valid_for_target_field = QLineEdit("")

            if not is_new_command:
                try:
                    conn = self.conn_manager.get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT userid, password, validForTargetLocations 
                        FROM Command 
                        WHERE id = ?
                    """, (command_id,))
                    additional_fields = cursor.fetchone()
                    
                    if additional_fields:
                        self.userid_field.setText(additional_fields['userid'] or "")
                        self.password_field.setText(additional_fields['password'] or "")
                        self.valid_for_target_field.setText(additional_fields['validForTargetLocations'] or "")
                except Exception as e:
                    logging.error(f"Failed to fetch additional fields: {e}")
                finally:
                    cursor.close()
                    conn.close()

            # Add `userID`, `password`, and `validForTargetLocations` as editable fields
            command_layout.addLayout(self.create_horizontal_layout("UserID", self.userid_field))
            command_layout.addLayout(self.create_horizontal_layout("Password", self.password_field))
            command_layout.addLayout(self.create_horizontal_layout("Valid For Target Locations", self.valid_for_target_field))

        # Create input fields for each parameter and add to layout
        for param_name in command_params_list:
            param_value = command_params.get(param_name, '') if not is_new_command else ''
            param_input = QLineEdit(param_value)
            self.param_widgets[(className, param_name)] = param_input
            command_layout.addLayout(self.create_horizontal_layout(param_name, param_input))

        command_group.setLayout(command_layout)
        self.vertical_layout.insertWidget(1, command_group)

    def save_commands(self):
        logging.info("Saving commands to database")
        try:
            conn = self.conn_manager.get_db_connection()
            cursor = conn.cursor()

            # Process each command widget, determining if it should be inserted or updated
            for command_widget in self.findChildren(QGroupBox):
                command_id = getattr(command_widget, "command_id", None)
                class_name = command_widget.objectName()
                command_type = self.command_type_dropdown.currentText()
                if command_id and command_id != 'new':
                    # Update existing command
                    self.update_command(cursor, command_id, class_name, command_type)
                else:
                    # Insert new command
                    self.insert_command(cursor, command_id, class_name, command_type)

                # Save additional fields if this is `AcsFiletransferPostCommandTksSend`
                if class_name == "de.bundesbank.acs.filetransfer.post.AcsFiletransferPostCommandTksSend" and command_id:
                    cursor.execute("""
                        UPDATE Command 
                        SET userid = ?, password = ?, validForTargetLocations = ?, commandType = ?
                        WHERE id = ?
                    """, (
                        self.userid_field.text(),
                        self.password_field.text(),
                        self.valid_for_target_field.text(),
                        self.command_type_dropdown.currentText(),
                        command_id
                    ))

            conn.commit()
            logging.info("Commands and parameters saved successfully")
        except Exception as e:
            conn.rollback()
            logging.error(f"Failed to save commands: {e}")
        finally:
            cursor.close()
            conn.close()

    def insert_command(self, cursor, command_id, class_name, command_type):
        logging.debug(f"Inserting new command for class: {class_name}")

        # Insert the new command and retrieve its ID
        cursor.execute("""
            INSERT INTO Command (communication_id, className, commandType)
            VALUES (?, ?, ?)
        """, (self.communication_id, class_name, command_type))
        command_id = cursor.lastrowid
        logging.debug(f"New command ID: {command_id}")

        # Insert each parameter into CommandParam table
        for order, param_name in enumerate(params.get(class_name, []), start=1):
            # Fetch parameter value from the param_widgets dictionary
            param_widget = self.param_widgets.get((class_name, param_name))
            if param_widget:
                param_value = param_widget.text()
                logging.debug(f"Inserting parameter - Name: {param_name}, Value: {param_value}, Order: {order}")
                cursor.execute("""
                    INSERT INTO CommandParam (command_id, param, paramName, paramOrder)
                    VALUES (?, ?, ?, ?)
                """, (command_id, param_value, param_name, order))

    def update_command(self,  cursor, command_id, class_name, command_type):
        logging.debug(f"Updating command ID: {command_id}, class: {class_name}")

        cursor.execute("""
            UPDATE Command 
            SET commandType = ?
            WHERE id = ?
            """, (
            command_type,
            command_id
            ))

        for param_name in params.get(class_name, []):
            # Access the QLineEdit widget directly using the param_widgets dictionary
            param_widget = self.param_widgets.get((class_name, param_name))
            if param_widget:
                param_value = param_widget.text()
                logging.debug(f"Updating parameter - Name: {param_name}, Value: {param_value}")
                cursor.execute("""
                    UPDATE CommandParam
                    SET param = ?
                    WHERE command_id = ? AND paramName = ?
                """, (param_value, command_id, param_name))
