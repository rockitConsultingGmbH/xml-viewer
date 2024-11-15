from gui.namelists_ui import NameListsWidget
from PyQt5.QtWidgets import QTreeWidgetItem, QMessageBox, QWidget
from PyQt5.QtCore import Qt
from common.config_manager import ConfigManager
from common.connection_manager import ConnectionManager
from gui.communication_ui import CommunicationUI
from database.utils import select_from_communication, insert_into_communication, delete_from_communication, insert_into_location, select_from_location, \
    select_from_command, insert_into_command, insert_into_commandparam, select_from_commandparam, insert_into_namelist, select_from_namelist, delete_from_namelist, insert_into_description, \
        select_from_description, insert_into_alternatename, select_from_alternatename, delete_from_alternatename_w_nameList_id

class NameListManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.conn_manager = ConnectionManager()
        self.config_manager = ConfigManager()

    def on_name_changed(self):
        self.name_changed = True

    def create_new_namelist(self):
        try:
            conn = self.main_window.conn_manager.get_db_connection()
            cursor = conn.cursor()
            new_namelist_id = insert_into_namelist(cursor, {"listName": "", "communication_id": "", "basicConfig_id": self.main_window.config_manager.config_id}).lastrowid
            conn.commit()
            conn.close()

            new_namelist_item = QTreeWidgetItem(["New Namelist"])
            new_namelist_item.setData(0, Qt.UserRole, new_namelist_id)
            self.main_window.namelist_item.insertChild(0, new_namelist_item)

            self.main_window.right_widget.setParent(None)
            name_list_ui = NameListsWidget(new_namelist_id)
            name_list_ui.name_updated.connect(self.update_namelist_in_tree)
            name_list_ui.list_name_input.textChanged.connect(self.on_name_changed)
            self.main_window.right_widget = name_list_ui
            self.main_window.right_widget.setObjectName("namelists_widget")
            self.main_window.splitter.addWidget(self.main_window.right_widget)
            self.main_window.splitter.setSizes([250, 1000])
            self.main_window.setCentralWidget(self.main_window.splitter)

            tree_widget = self.main_window.left_widget.layout().itemAt(0).widget()
            tree_widget.setCurrentItem(new_namelist_item)

            self.main_window.unsaved_changes = True
            self.main_window.current_namelist_id = new_namelist_id
            self.main_window.name_changed = False
        except Exception as e:
            QMessageBox.critical(self.main_window, "Error", f"An error occurred: {str(e)}")

    def delete_new_namelist(self):
        try:
            conn = self.main_window.conn_manager.get_db_connection()
            cursor = conn.cursor()
            namelist_id = self.main_window.current_namelist_id
            delete_from_namelist(cursor, namelist_id)
            delete_from_alternatename_w_nameList_id(cursor, namelist_id)
            conn.commit()
            conn.close()

            for i in range(self.main_window.namelist_item.childCount()):
                child_item = self.main_window.namelist_item.child(i)
                if child_item.data(0, Qt.UserRole) == self.main_window.current_namelist_id:
                    self.main_window.namelist_item.removeChild(child_item)
                    break

            self.main_window.right_widget.setParent(None)
            self.main_window.right_widget = QWidget()
            self.main_window.right_widget.setObjectName("right_widget")
            self.main_window.splitter.addWidget(self.main_window.right_widget)
            self.main_window.splitter.setSizes([250, 1000])
            self.main_window.setCentralWidget(self.main_window.splitter)

            self.main_window.unsaved_changes = False
            self.main_window.current_namelist_id = None
        except Exception as e:
            QMessageBox.critical(self.main_window, "Error", f"An error occurred while deleting the nameList: {str(e)}")

    def delete_namelist(self, namelist_id):
        reply = QMessageBox.question(
            self.main_window,
            "Confirm Deletion",
            "Are you sure you want to delete this NameList?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            conn = self.main_window.conn_manager.get_db_connection()
            cursor = conn.cursor()
            delete_from_namelist(cursor, namelist_id)
            delete_from_alternatename_w_nameList_id(cursor, namelist_id)
            conn.commit()
            conn.close()

            next_item = None
            for i in range(self.main_window.namelist_item.childCount()):
                child_item = self.main_window.namelist_item.child(i)
                if child_item.data(0, Qt.UserRole) == namelist_id:
                    index = self.main_window.namelist_item.indexOfChild(child_item)
                    self.main_window.namelist_item.removeChild(child_item)
                    if self.main_window.namelist_item.childCount() > 0:
                        next_item = self.main_window.namelist_item.child(0)
                    break

            if next_item:
                self.main_window.on_item_clicked(next_item)
                tree_widget = self.main_window.left_widget.layout().itemAt(0).widget()
                tree_widget.setCurrentItem(next_item)
            else:
                self.main_window.right_widget.setParent(None)
                self.main_window.right_widget = QWidget()
                self.main_window.splitter.addWidget(self.main_window.right_widget)

            QMessageBox.information(self.main_window, "Deleted", "Namelist deleted successfully.")

    def delete_selected_namelist(self):
        tree_widget = self.main_window.left_widget.layout().itemAt(0).widget()
        current_item = tree_widget.currentItem()
        if current_item and current_item.parent() == self.main_window.namelist_item:
            nameList_id = current_item.data(0, Qt.UserRole)
            self.delete_namelist(nameList_id)

    def update_namelist_in_tree(self, nameList_id, new_name):
        for i in range(self.main_window.namelist_item.childCount()):
            child_item = self.main_window.namelist_item.child(i)
            if child_item.data(0, Qt.UserRole) == nameList_id:
                child_item.setText(0, new_name)
                break

    def duplicate_selected_namelist(self):
        tree_widget = self.main_window.left_widget.layout().itemAt(0).widget()
        selected_item = tree_widget.currentItem()

        if not selected_item:
            QMessageBox.warning(self.main_window, "No Selection", "Please select a namelist to duplicate.")
            return

        namelist_id = selected_item.data(0, Qt.UserRole)

        conn = self.conn_manager.get_db_connection()
        cursor = conn.cursor()
        name_list = select_from_namelist(cursor, namelist_id).fetchone()

        if not name_list:
            QMessageBox.critical(self.main_window, "Error", "Selected namelist not found in the database.")
            conn.close()
            return

        # Duplicate namelist data and insert the new namelist
        duplicate_name_list_data = self.duplicate_data(name_list)
        duplicate_name_list_data['communication_id'] = name_list['communication_id']   #Keep original communication_id
        new_name_list_id = insert_into_namelist(cursor, duplicate_name_list_data).lastrowid

        # Duplicate alternate names linked to the original namelist
        alternate_names = select_from_alternatename(cursor, namelist_id).fetchall()
        for alternate_name in alternate_names:
            duplicate_alternate_name_data = self.duplicate_data(alternate_name)
            duplicate_alternate_name_data['nameList_id'] = new_name_list_id
            insert_into_alternatename(cursor, duplicate_alternate_name_data)

        # Commit transaction and close connection
        conn.commit()
        conn.close()

        # Add the duplicated namelist as a new item in the tree
        self.create_duplicated_item(selected_item, duplicate_name_list_data, new_name_list_id)

    def duplicate_data(self, data):
        """Duplicate data dictionary with adjustments for copying."""
        duplicate_data = dict(data)
        if 'name' in duplicate_data:
            duplicate_data['name'] += " Copy"
        if 'listName' in duplicate_data:
            duplicate_data['listName'] += " Copy"
        if 'id' in duplicate_data:
            duplicate_data.pop('id')   #Remove 'id' to allow a new ID to be generated
        return duplicate_data

    def create_duplicated_item(self, selected_item, duplicate_data, new_id):
        """Insert duplicated item in the tree below the selected item."""
        duplicated_item = QTreeWidgetItem([duplicate_data['listName']])
        duplicated_item.setData(0, Qt.UserRole, new_id)

        parent_item = selected_item.parent()
        if not parent_item:
            parent_item = self.main_window.namelist_item

        selected_index = parent_item.indexOfChild(selected_item)
        parent_item.insertChild(selected_index + 1, duplicated_item)

        # Expand to display the new duplicated item
        parent_item.setExpanded(True)

