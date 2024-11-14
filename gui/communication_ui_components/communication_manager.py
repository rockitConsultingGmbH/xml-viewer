import logging
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidgetItem, QMessageBox, QWidget
from common.config_manager import ConfigManager
from common.connection_manager import ConnectionManager
from gui.communication_ui import CommunicationUI
from database.utils import select_from_communication, insert_into_communication, delete_from_communication, insert_into_location, select_from_location, \
    select_from_command, insert_into_command, insert_into_commandparam, select_from_commandparam, insert_into_namelist, select_from_namelist_w_communication_id, insert_into_description, \
        select_from_description, insert_into_alternatename, select_from_alternatename

class CommunicationManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.conn_manager = ConnectionManager()
        self.config_manager = ConfigManager()
        
    def create_new_communication(self):
        try:
            conn = self.main_window.conn_manager.get_db_connection()
            cursor = conn.cursor()
            new_communication_id = insert_into_communication(cursor, {"name": "", "basicConfig_id": self.main_window.config_manager.config_id}).lastrowid
            conn.commit()
            conn.close()

            new_item = QTreeWidgetItem(["New Communication"])
            new_item.setData(0, Qt.UserRole, new_communication_id)
            self.main_window.communication_config_item.insertChild(0, new_item)

            self.main_window.right_widget.setParent(None)
            communication_ui = CommunicationUI(new_communication_id)
            communication_ui.name_updated.connect(self.update_communication_in_tree)
            communication_ui.name_input.textChanged.connect(self.main_window.on_name_changed)
            self.main_window.right_widget = communication_ui
            self.main_window.right_widget.setObjectName("communications_widget")
            self.main_window.splitter.addWidget(self.main_window.right_widget)
            self.main_window.splitter.setSizes([250, 1000])
            self.main_window.setCentralWidget(self.main_window.splitter)

            tree_widget = self.main_window.left_widget.layout().itemAt(0).widget()
            tree_widget.setCurrentItem(new_item)

            self.main_window.unsaved_changes = True
            self.main_window.current_communication_id = new_communication_id
            self.main_window.name_changed = False
        except Exception as e:
            QMessageBox.critical(self.main_window, "Error", f"An error occurred: {str(e)}")

    def update_communication_in_tree(self, communication_id, new_name):
        for i in range(self.main_window.communication_config_item.childCount()):
            child_item = self.main_window.communication_config_item.child(i)
            if child_item.data(0, Qt.UserRole) == communication_id:
                child_item.setText(0, new_name)
                break

    def delete_new_communication(self):
        try:
            conn = self.main_window.conn_manager.get_db_connection()
            cursor = conn.cursor()
            delete_from_communication(cursor, self.main_window.current_communication_id)
            conn.commit()
            conn.close()

            for i in range(self.main_window.communication_config_item.childCount()):
                child_item = self.main_window.communication_config_item.child(i)
                if child_item.data(0, Qt.UserRole) == self.main_window.current_communication_id:
                    self.main_window.communication_config_item.removeChild(child_item)
                    break

            self.main_window.right_widget.setParent(None)
            self.main_window.right_widget = QWidget()
            self.main_window.right_widget.setObjectName("right_widget")
            self.main_window.splitter.addWidget(self.main_window.right_widget)
            self.main_window.splitter.setSizes([250, 1000])
            self.main_window.setCentralWidget(self.main_window.splitter)

            self.main_window.unsaved_changes = False
            self.main_window.current_communication_id = None
        except Exception as e:
            QMessageBox.critical(self.main_window, "Error", f"An error occurred while deleting the communication: {str(e)}")

    def delete_communication(self, communication_id):
        reply = QMessageBox.question(
            self.main_window,
            "Confirm Deletion",
            "Are you sure you want to delete this communication?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            conn = self.main_window.conn_manager.get_db_connection()
            cursor = conn.cursor()
            delete_from_communication(cursor, communication_id)
            conn.commit()
            conn.close()

            # Remove the item from the tree and refresh the tree view
            next_item = None
            for i in range(self.main_window.communication_config_item.childCount()):
                child_item = self.main_window.communication_config_item.child(i)
                if child_item.data(0, Qt.UserRole) == communication_id:
                    self.main_window.communication_config_item.removeChild(child_item)
                    if self.main_window.communication_config_item.childCount() > 0:
                        next_item = self.main_window.communication_config_item.child(0)
                    break

            # Refresh the tree_widget to reflect changes
            tree_widget = self.main_window.left_widget.layout().itemAt(0).widget()
            tree_widget.update()
            tree_widget.repaint()

            if next_item:
                self.main_window.on_item_clicked(next_item)
                tree_widget.setCurrentItem(next_item)
            else:
                self.main_window.right_widget.setParent(None)
                self.main_window.right_widget = QWidget()
                self.main_window.splitter.addWidget(self.main_window.right_widget)

            QMessageBox.information(self.main_window, "Deleted", "Communication deleted successfully.")

    def delete_new_namelist(self):
        self.delete_new_communication()

    def delete_selected_communication(self):
        tree_widget = self.main_window.left_widget.layout().itemAt(0).widget()
        current_item = tree_widget.currentItem()
        if current_item and current_item.parent() == self.main_window.communication_config_item:
            communication_id = current_item.data(0, Qt.UserRole)
            self.delete_communication(communication_id)

    def duplicate_selected_communication(self):
        tree_widget = self.main_window.left_widget.layout().itemAt(0).widget()
        selected_item = tree_widget.currentItem()

        if not selected_item:
            QMessageBox.warning(self.main_window, "No Selection", "Please select a communication to duplicate.")
            return

        communication_id = selected_item.data(0, Qt.UserRole)

        conn = self.conn_manager.get_db_connection()
        cursor = conn.cursor()
        communication = select_from_communication(cursor, communication_id, self.config_manager.config_id).fetchone()
        descriptions = select_from_description(cursor, communication_id).fetchall()
        locations = select_from_location(cursor, communication_id).fetchall()
        commands = select_from_command(cursor, communication_id).fetchall()
        #name_list = select_from_namelist_w_communication_id(cursor, communication_id).fetchone()

        if not communication:
            QMessageBox.critical(self.main_window, "Error", "Selected communication not found in the database.")
            conn.close()
            return

        duplicate_communication_data = self.duplicate_data(cursor, communication)
        new_communication_id = insert_into_communication(cursor, duplicate_communication_data).lastrowid

        for description in descriptions:
            duplicate_description_data = self.duplicate_data(cursor, description)
            duplicate_description_data['communication_id'] = new_communication_id
            insert_into_description(cursor, duplicate_description_data)

        #if name_list:
        #    duplicate_name_list_data = self.duplicate_data(cursor, name_list)
        #    duplicate_name_list_data['communication_id'] = new_communication_id
        #    new_name_list_id = insert_into_namelist(cursor, duplicate_name_list_data).lastrowid
        #
        #    alternate_names = select_from_alternatename(cursor, name_list['id']).fetchall()
        #    for alternate_name in alternate_names:
        #        duplicate_alternate_name_data = self.duplicate_data(cursor, alternate_name)
        #        duplicate_alternate_name_data['nameList_id'] = new_name_list_id
        #        insert_into_alternatename(cursor, duplicate_alternate_name_data)

        for location in locations:
            duplicate_location_data = self.duplicate_data(cursor, location)
            duplicate_location_data['communication_id'] = new_communication_id
            insert_into_location(cursor, duplicate_location_data)

        for command in commands:
            duplicate_command_data = self.duplicate_data(cursor, command)
            duplicate_command_data['communication_id'] = new_communication_id
            new_command_id = insert_into_command(cursor, duplicate_command_data).lastrowid
            commandparams = select_from_commandparam(cursor, command['id']).fetchall()

            for commandparam in commandparams:
                duplicate_commandparam_data = self.duplicate_data(cursor, commandparam)
                duplicate_commandparam_data['command_id'] = new_command_id
                insert_into_commandparam(cursor, duplicate_commandparam_data)
    
        conn.commit()
        conn.close()

        self.create_duplicated_item(selected_item, duplicate_communication_data, new_communication_id)

    def duplicate_data(self, cursor, data):
        duplicate_data = dict(data)
        if 'name' in duplicate_data:
            duplicate_data['name'] += " Copy"
        if 'alternateNameList' in duplicate_data:
            duplicate_data['alternateNameList'] = ""
        if 'listName' in duplicate_data:
            duplicate_data['listName'] += " Copy"
        if 'id' in duplicate_data:
            duplicate_data.pop('id')
        return duplicate_data

    def create_duplicated_item(self, selected_item, duplicate_data, new_communication_id):
        # Create the duplicated item and set its data
        duplicated_item = QTreeWidgetItem([duplicate_data['name']])
        duplicated_item.setData(0, Qt.UserRole, new_communication_id)

        # Find the selected item's index in its parent and insert duplicated item just after it
        parent_item = selected_item.parent()
        if not parent_item:
            parent_item = self.main_window.communication_config_item

        selected_index = parent_item.indexOfChild(selected_item)
        parent_item.insertChild(selected_index + 1, duplicated_item)

        # Expand the parent item to show the new duplicated item
        parent_item.setExpanded(True)