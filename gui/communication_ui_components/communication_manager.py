from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidgetItem, QMessageBox, QWidget
from gui.communication_ui import CommunicationUI

class CommunicationManager:
    def __init__(self, main_window):
        self.main_window = main_window

    def create_new_communication(self):
        try:
            conn = self.main_window.conn_manager.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Communication (name, basicConfig_id) VALUES (?, ?)",
                           ("", self.main_window.config_manager.config_id))
            conn.commit()
            new_communication_id = cursor.lastrowid
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
            cursor.execute("DELETE FROM Communication WHERE id = ?", (self.main_window.current_communication_id,))
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
            cursor.execute("DELETE FROM Communication WHERE id = ?", (communication_id,))
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
            tree_widget.update()  # Ensures the widget is visually updated
            tree_widget.repaint()  # Forces a repaint if needed

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
