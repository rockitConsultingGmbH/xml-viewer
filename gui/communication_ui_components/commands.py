from PyQt5.QtWidgets import QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QComboBox, QGroupBox
from PyQt5.QtCore import Qt

from common.connection_manager import ConnectionManager
from database.utils import select_from_command, select_from_commandparam

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
        # Initialize fields for new command UI
        self.dropdown = QComboBox()
        self.param_widgets = {}
        self.command_group = None

        # Add dropdown and "+" button for creating a new command at the top
        self.add_new_command_controls()
        # Load and display existing commands from the database after new command controls
        self.generate_command_ui()

    def add_new_command_controls(self):
        # Create dropdown for new commands and "+" button
        self.dropdown.addItems(params.keys())
        self.dropdown.setFixedSize(550, 30)  # Adjust width of dropdown list here

        plus_button = QPushButton("+")
        plus_button.setFixedSize(20, 20)
        plus_button.clicked.connect(self.add_new_command)

        # Horizontal layout for dropdown and "+" button
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.dropdown)
        button_layout.addWidget(plus_button)
        button_layout.setAlignment(Qt.AlignLeft)

        # Insert new command controls at the top of the layout
        self.vertical_layout.insertLayout(0, button_layout)

    def add_new_command(self):
        # Get the selected class name from the dropdown
        selected_classname = self.dropdown.currentText()
        if selected_classname:
            self.display_fields_for_classname(selected_classname)

    def display_fields_for_classname(self, className):
        # Clear any previous temporary fields for new commands
        self.clear_command_fields()

        # Create a new command group box for the selected class
        self.command_group = QGroupBox()
        command_layout = QVBoxLayout()
        
        # Add label for the new command at the top of the group box
        command_label = QLabel(f"<b>New Command: {className.split('.')[-1]}</b>")
        command_label.setAlignment(Qt.AlignLeft)
        command_layout.addWidget(command_label)

        # Generate fields for each parameter
        for param in params.get(className, []):
            param_input = QLineEdit()
            param_input.setFixedSize(350, 30)
            param_input.setObjectName(f"{param}_{className}")

            # Store parameter widget reference
            self.param_widgets[param] = param_input
            command_layout.addLayout(self.create_horizontal_layout(param, param_input))

        self.command_group.setLayout(command_layout)

        # Insert the new command group at the top of the layout
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
        # Remove existing temporary fields for a new command if present
        if self.command_group:
            self.command_group.setParent(None)
            self.command_group.deleteLater()
            self.command_group = None
        self.param_widgets.clear()

    def generate_command_ui(self):
        # Pull existing command fields from the database
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
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

    def get_command_params(self, command_id):
        # Fetch command parameters from the database
        try:
            conn = self.conn_manager.get_db_connection()
            cursor = conn.cursor()
            rows = select_from_commandparam(cursor, command_id).fetchall()
            return {param['paramName']: param['param'] for param in rows}
        except Exception as e:
            print(f"Error: {e}")
            return {}
        finally:
            cursor.close()
            conn.close()

    def generate_command_classname(self, className):
        # Display the class name in the UI
        command_classname_input = QLineEdit(className)
        command_classname_input.setReadOnly(True)
        h_layout = self.create_horizontal_layout("Classname", command_classname_input, is_classname=True)
        return h_layout

    def generate_command_widget(self, command_id):
        # Create UI components for each command
        command_widget = QWidget()
        command_box = QVBoxLayout(command_widget)
        return command_widget, command_box

    def generate_command_params(self, className, command_id):
        # Set up UI components for database-loaded commands
        command_widget, command_box = self.generate_command_widget(command_id)
        
        # Retrieve params for the given command_id
        command_params = self.get_command_params(command_id)
        command_params_list = params.get(className, [])

        # Display class name as label
        box_label = QLabel(f"<b>{className.split('.')[-1]}</b>")
        box_label.setTextFormat(Qt.RichText)
        box_label.setAlignment(Qt.AlignLeft)
        command_box.addWidget(box_label)
        command_box.addLayout(self.generate_command_classname(className))

        # Create fields for each param in command_params_list and populate with command_params values
        for param_name in command_params_list:
            param_value = command_params.get(param_name, '')
            param_input = QLineEdit(param_value)
            param_input.setObjectName(f"{param_name}_{command_id}")
            command_box.addLayout(self.create_horizontal_layout(param_name, param_input))

        # Add command widget with parameters to main layout
        self.vertical_layout.addWidget(command_widget)

    def save_commands(self):
        try:
            # Establish a connection for the save operation
            conn = self.conn_manager.get_db_connection()
            cursor = conn.cursor()

            # Loop through each command to determine whether to insert or update
            for command_widget in self.vertical_layout.children():
                if isinstance(command_widget, QGroupBox):  # Ensure we're working with command groups
                    command_id = getattr(command_widget, "command_id", None)  # Command ID if exists
                    class_name = command_widget.objectName()  # Class name used as unique identifier
                    
                    if command_id:  # Update existing command
                        self.update_command(cursor, command_id, class_name, command_widget)
                    else:  # Insert new command
                        self.insert_command(cursor, class_name, command_widget)

            # Commit all changes
            conn.commit()
            #QMessageBox.information(self, "Success", "Commands and parameters saved successfully.")
        except Exception as e:
            conn.rollback()
            #QMessageBox.critical(self, "Error", f"Failed to save commands: {e}")
        finally:
            cursor.close()
            conn.close()

    def update_command(self, cursor, command_id, class_name, command_widget):
        # Update the command information in Command table
        cursor.execute("""
            UPDATE Command
            SET className = ?
            WHERE id = ?
        """, (class_name, command_id))

        # Update or insert parameters in CommandParam table
        for param_name, param_widget in self.param_widgets.items():
            param_value = param_widget.text()
            cursor.execute("""
                INSERT INTO CommandParam (command_id, param, paramName)
                VALUES (?, ?, ?)
                ON CONFLICT(command_id, paramName) DO UPDATE SET param = excluded.param
            """, (command_id, param_value, param_name))

    def insert_command(self, cursor, class_name, command_widget):
        # Insert new command into Command table
        cursor.execute("""
            INSERT INTO Command (communication_id, className)
            VALUES (?, ?)
        """, (self.communication_id, class_name))
        
        # Get the ID of the newly inserted command
        command_id = cursor.lastrowid

        # Insert parameters for the new command in CommandParam table
        for order, param_name in enumerate(params.get(class_name, []), start=1):
            param_value = self.param_widgets[param_name].text()
            cursor.execute("""
                INSERT INTO CommandParam (command_id, param, paramName, paramOrder)
                VALUES (?, ?, ?, ?)
            """, (command_id, param_value, param_name, order))

