import sqlite3

from common.connection_manager import ConnectionManager


class CommandParamTableData: 
    def __init__(self, parent_widget=None):
        self.conn_manager = ConnectionManager().get_instance()
        self.parent_widget = parent_widget

    def set_parent_widget(self, parent_widget):
        self.parent_widget = parent_widget

    def save_command_params(self, command_id):
            """
            Reads each parameter field from the UI and saves updates to the CommandParam table.
            """
            try:
                conn = self.conn_manager.get_db_connection()
                cursor = conn.cursor()
                
                # Retrieve existing command parameters for the command_id
                existing_params = self.get_command_params(command_id)
                
                # Loop through each parameter input in the UI and update/insert accordingly
                for param_name, param_input in self.param_widgets.items():
                    param_value = param_input.text()  # Get the current value in the QLineEdit
                    
                    # Check if this param_name exists in the existing_params (update case)
                    if param_name in existing_params:
                        cursor.execute("""
                            UPDATE CommandParam
                            SET param = ?
                            WHERE command_id = ? AND paramName = ?
                        """, (param_value, command_id, param_name))
                    else:
                        # Insert new parameter if it doesn't exist
                        cursor.execute("""
                            INSERT INTO CommandParam (command_id, param, paramName, paramOrder)
                            VALUES (?, ?, ?, ?)
                        """, (command_id, param_value, param_name, len(existing_params) + 1))

                conn.commit()
                print("Command parameters successfully saved.")
            
            except sqlite3.Error as e:
                conn.rollback()
                print(f"An error occurred while saving command parameters: {e}")
            
            finally:
                cursor.close()
                conn.close()

    # get_command_params function
    def get_command_params(self, command_id):
        try:
            conn = self.conn_manager.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT paramName, param FROM CommandParam WHERE command_id = ?
            """, (command_id,))
            rows = cursor.fetchall()
            return {row['paramName']: row['param'] for row in rows}
        except Exception as e:
            print(f"An error occurred: {e}")
            return {}
        finally:
            cursor.close()
            conn.close()