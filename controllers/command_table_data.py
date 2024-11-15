import sqlite3

from common.connection_manager import ConnectionManager
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class CommandParamTableData: 
    def __init__(self, parent_widget=None):
        self.conn_manager = ConnectionManager()
        self.parent_widget = parent_widget

    def set_parent_widget(self, parent_widget):
        self.parent_widget = parent_widget

    def save_command_params(self, command_id):
            try:
                conn = self.conn_manager.get_db_connection()
                cursor = conn.cursor()
                
                existing_params = self.get_command_params(command_id)
                
                for param_name, param_input in self.param_widgets.items():
                    param_value = param_input.text()
                    
                    if param_name in existing_params:
                        cursor.execute("""
                            UPDATE CommandParam
                            SET param = ?
                            WHERE command_id = ? AND paramName = ?
                        """, (param_value, command_id, param_name))
                    else:
                        cursor.execute("""
                            INSERT INTO CommandParam (command_id, param, paramName, paramOrder)
                            VALUES (?, ?, ?, ?)
                        """, (command_id, param_value, param_name, len(existing_params) + 1))

                conn.commit()
                logging.debug("Command parameters successfully saved.")
            
            except sqlite3.Error as e:
                conn.rollback()
                logging.debug(f"An error occurred while saving command parameters: {e}")
            
            finally:
                cursor.close()
                conn.close()

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
            logging.debug(f"An error occurred: {e}")
            return {}
        finally:
            cursor.close()
            conn.close()