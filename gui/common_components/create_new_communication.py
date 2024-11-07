from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidgetItem, QMessageBox, QWidget
from gui.common_components.communication_popup_warnings import show_unsaved_changes_warning
from gui.communication_ui import CommunicationUI


def create_new_communication(main_window):
    try:
        conn = main_window.conn_manager.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Communication (name, basicConfig_id) VALUES (?, ?)",
                       ("", main_window.config_manager.config_id))
        conn.commit()
        new_communication_id = cursor.lastrowid
        conn.close()

        new_item = QTreeWidgetItem(["New Communication"])
        new_item.setData(0, Qt.UserRole, new_communication_id)
        main_window.communication_config_item.insertChild(0, new_item)

        main_window.right_widget.setParent(None)
        communication_ui = CommunicationUI(new_communication_id)
        communication_ui.name_updated.connect(main_window.update_communication_in_tree)
        communication_ui.name_input.textChanged.connect(main_window.on_name_changed)
        main_window.right_widget = communication_ui
        main_window.right_widget.setObjectName("communications_widget")
        main_window.splitter.addWidget(main_window.right_widget)
        main_window.splitter.setSizes([250, 1000])
        main_window.setCentralWidget(main_window.splitter)

        tree_widget = main_window.left_widget.layout().itemAt(0).widget()
        tree_widget.setCurrentItem(new_item)

        main_window.unsaved_changes = True
        main_window.current_communication_id = new_communication_id
        main_window.name_changed = False
    except Exception as e:
        QMessageBox.critical(main_window, "Error", f"An error occurred: {str(e)}")


def on_name_changed(main_window):
    main_window.name_changed = True


def delete_new_communication(main_window):
    try:
        conn = main_window.conn_manager.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Communication WHERE id = ?", (main_window.current_communication_id,))
        conn.commit()
        conn.close()

        for i in range(main_window.communication_config_item.childCount()):
            child_item = main_window.communication_config_item.child(i)
            if child_item.data(0, Qt.UserRole) == main_window.current_communication_id:
                main_window.communication_config_item.removeChild(child_item)
                break

        main_window.right_widget.setParent(None)
        main_window.right_widget = QWidget()
        main_window.right_widget.setObjectName("right_widget")
        main_window.splitter.addWidget(main_window.right_widget)
        main_window.splitter.setSizes([250, 1000])
        main_window.setCentralWidget(main_window.splitter)

        main_window.unsaved_changes = False
        main_window.current_communication_id = None
    except Exception as e:
        QMessageBox.critical(main_window, "Error", f"An error occurred while deleting the communication: {str(e)}")


def delete_communication(main_window, communication_id):
    reply = QMessageBox.question(
        main_window,
        "Confirm Deletion",
        "Are you sure you want to delete this communication?",
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )

    if reply == QMessageBox.Yes:
        conn = main_window.conn_manager.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Communication WHERE id = ?", (communication_id,))
        conn.commit()
        conn.close()

        next_item = None
        for i in range(main_window.communication_config_item.childCount()):
            child_item = main_window.communication_config_item.child(i)
            if child_item.data(0, Qt.UserRole) == communication_id:
                index = main_window.communication_config_item.indexOfChild(child_item)
                main_window.communication_config_item.removeChild(child_item)
                if main_window.communication_config_item.childCount() > 0:
                    next_item = main_window.communication_config_item.child(0)
                break

        if next_item:
            main_window.on_item_clicked(next_item)
            tree_widget = main_window.left_widget.layout().itemAt(0).widget()
            tree_widget.setCurrentItem(next_item)
        else:
            main_window.right_widget.setParent(None)
            main_window.right_widget = QWidget()
            main_window.splitter.addWidget(main_window.right_widget)

        QMessageBox.information(main_window, "Deleted", "Communication deleted successfully.")
