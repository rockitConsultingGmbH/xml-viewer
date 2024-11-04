from gui.namelists_ui import NameListsWidget
from PyQt5.QtWidgets import QTreeWidgetItem, QMessageBox, QWidget
from PyQt5.QtCore import Qt

def on_name_changed(main_window):
    main_window.name_changed = True

def create_new_namelist(main_window):
    try:
        conn = main_window.conn_manager.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO NameList (listName, basicConfig_id) VALUES (?, ?)",
                       ("New Namelist", main_window.config_manager.config_id))
        conn.commit()
        new_namelist_id = cursor.lastrowid
        conn.close()

        main_window.right_widget.setParent(None)
        name_list_ui = NameListsWidget(new_namelist_id)
        name_list_ui.name_updated.connect(main_window.update_namelist_in_tree)
        name_list_ui.list_name_input.textChanged.connect(main_window.on_name_changed)
        main_window.right_widget = name_list_ui
        main_window.right_widget.setObjectName("namelists_widget")
        main_window.splitter.addWidget(main_window.right_widget)
        main_window.splitter.setSizes([250, 1000])

        new_namelist_item = QTreeWidgetItem(["New Namelist"])
        new_namelist_item.setData(0, Qt.UserRole, new_namelist_id)
        main_window.namelist_item.insertChild(0, new_namelist_item)
        tree_widget = main_window.left_widget.layout().itemAt(0).widget()
        tree_widget.setCurrentItem(new_namelist_item)

    except Exception as e:
        QMessageBox.critical(main_window, "Error", f"An error occurred: {str(e)}")

def delete_selected_namelist(main_window, namelist_id):
    reply = QMessageBox.question(
        main_window,
        "Confirm Deletion",
        "Are you sure you want to delete this NameList?",
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )

    if reply == QMessageBox.Yes:
        conn = main_window.conn_manager.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM NameList WHERE id = ?", (namelist_id,))
        conn.commit()
        conn.close()

        next_item = None
        for i in range(main_window.namelist_item.childCount()):
            child_item = main_window.namelist_item.child(i)
            if child_item.data(0, Qt.UserRole) == namelist_id:
                index = main_window.namelist_item.indexOfChild(child_item)
                main_window.namelist_item.removeChild(child_item)
                if main_window.namelist_item.childCount() > 0:
                    next_item = main_window.namelist_item.child(0)
                break

        if next_item:
            main_window.on_item_clicked(next_item)
            tree_widget = main_window.left_widget.layout().itemAt(0).widget()
            tree_widget.setCurrentItem(next_item)
        else:
            main_window.right_widget.setParent(None)
            main_window.right_widget = QWidget()
            main_window.splitter.addWidget(main_window.right_widget)

        QMessageBox.information(main_window, "Deleted", "Namelist deleted successfully.")