import logging
import sqlite3
import sys
import lxml
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QSplitter, QWidget, QVBoxLayout, QTreeWidget, \
    QTreeWidgetItem, QMessageBox, QFileDialog, QMenu, QLineEdit

from gui.common_components.communication_popup_warnings import show_unsaved_changes_warning
from gui.common_components.create_new_communication import create_new_communication, on_name_changed, delete_new_communication, delete_communication
from gui.common_components.create_new_namelist import create_new_namelist, on_name_changed, delete_selected_namelist
from utils.empty_database import empty_database
from gui.import_xml_dialog_window import FileDialog
from gui.communication_ui import CommunicationUI
from gui.basic_configuration_ui import BasicConfigurationWidget
from gui.lzb_configuration_ui import LZBConfigurationWidget
from gui.mq_configuration_ui import MQConfigurationWidget

from common.connection_manager import ConnectionManager
from common.config_manager import ConfigManager

from gui.namelists_ui import NameListsWidget
from utils.export_db_to_xml.db_to_xml import export_to_xml as export_to_xml_function

from gui.common_components.stylesheet_loader import load_stylesheet

logging.basicConfig(level=logging.DEBUG)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.input_field = None
        self.recent_files = []
        self.basic_config_item = None
        self.conn_manager = ConnectionManager()
        self.config_manager = ConfigManager()
        self.version = self.config_manager.get_property_from_properties("version")
        self.app_name = self.config_manager.get_property_from_properties("appName")

        logging.debug(f"Version: {self.version}")
        logging.debug(f"App Name: {self.app_name}")

        self.resize(1800, 900)
        self.setWindowTitle(self.app_name)

        screen = QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

        self.left_widget = QWidget()
        self.right_widget = QWidget()
        self.left_widget.setObjectName("left_widget")
        self.right_widget.setObjectName("right_widget")

        self.left_widget.setFixedWidth(400)

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.left_widget)
        self.splitter.addWidget(self.right_widget)
        self.splitter.setSizes([400, 1000])
        self.setCentralWidget(self.splitter)

        load_stylesheet(self, "css/tree_widget_styling.qss")

        self.create_menu()

    def create_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu('File')
        open_xml_action = QAction('Open', self)
        open_xml_action.setShortcut('Ctrl+O')
        open_xml_action.setStatusTip('Ctrl+O')
        file_menu.addAction(open_xml_action)
        open_xml_action.triggered.connect(self.open_xml)

        file_menu.addSeparator()

        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('Ctrl+S')
        file_menu.addAction(save_action)
        save_action.triggered.connect(self.save_config)

        export_action = QAction('Save As...', self)
        export_action.setShortcut('Ctrl+E')
        export_action.setStatusTip('Ctrl+E')
        file_menu.addAction(export_action)
        export_action.triggered.connect(self.export_config)

        file_menu.addSeparator()
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+X')
        exit_action.setStatusTip('Ctrl+X')
        file_menu.addAction(exit_action)
        exit_action.triggered.connect(self.exit_application)

        edit_menu = menubar.addMenu('Edit')

        copy_action = QAction('Copy', self)
        copy_action.setShortcut('Ctrl+C')
        copy_action.setStatusTip('Ctrl+C')
        edit_menu.addAction(copy_action)
        copy_action.triggered.connect(self.copy_text)

        delete_action = QAction('Delete', self)
        delete_action.setShortcut('Ctrl+D')
        delete_action.setStatusTip('Ctrl+D')
        edit_menu.addAction(delete_action)
        delete_action.triggered.connect(self.delete_text)

        select_all_action = QAction('Select all', self)
        select_all_action.setShortcut('Ctrl+A')
        select_all_action.setStatusTip('Ctrl+A')
        edit_menu.addAction(select_all_action)
        select_all_action.triggered.connect(self.select_all_text)

        edit_menu.addSeparator()

        communication_menu = edit_menu.addMenu('Communication')
        create_communication_action = QAction('New...', self)
        communication_menu.addAction(create_communication_action)
        create_communication_action.triggered.connect(lambda: create_new_communication(self))

        delete_communication_action = QAction('Delete selected', self)
        communication_menu.addAction(delete_communication_action)
        delete_communication_action.triggered.connect(self.delete_selected_communication)


        namelist_menu = edit_menu.addMenu('NameList')
        create_namelist_action = QAction('New...', self)
        namelist_menu.addAction(create_namelist_action)
        create_namelist_action.triggered.connect(lambda: create_new_namelist(self))

        delete_namelist_action = QAction('Delete selected', self)
        namelist_menu.addAction(delete_namelist_action)
        delete_namelist_action.triggered.connect(self.delete_selected_namelist)
    
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)

        guide_action = QAction("Guide", self)
        guide_action.setEnabled(False)
        #guide_action.triggered.connect(self.show_about)

        menubar = self.menuBar()
        help_menu = menubar.addMenu("Help")
        help_menu.addAction(about_action)
        help_menu.addAction(guide_action)

    def show_about(self):
        QMessageBox.about(self, "About", f"{self.app_name}: v{self.version }")

    def copy_text(self):
        widget = self.focusWidget()
        if isinstance(widget, QLineEdit):
            widget.copy()

    def delete_text(self):
        widget = self.focusWidget()
        if isinstance(widget, QLineEdit):
            cursor = widget.cursorPosition()
            if widget.hasSelectedText():
                widget.del_()
            else:
                widget.backspace()

    def select_all_text(self):
        widget = self.focusWidget()
        if isinstance(widget, QLineEdit):
            widget.selectAll()

    def on_name_changed(self):
        on_name_changed(self)

    def open_xml(self):
        dialog = FileDialog(self)
        if dialog.exec_():
            if self.recent_files:
                self.reinitialize()
            self.display_db_tables()

            self.load_basic_config_view()

            if self.basic_config_item:
                tree_widget = self.left_widget.layout().itemAt(0).widget()
                tree_widget.setCurrentItem(self.basic_config_item)

    def reinitialize(self):
        if self.right_widget.layout() is not None:
            old_layout = self.right_widget.layout()
            QWidget().setLayout(old_layout)
        self.right_widget.setParent(None)
        self.right_widget = QWidget()
        self.right_widget.setObjectName("right_widget")
        self.splitter.addWidget(self.right_widget)

        if self.left_widget.layout() is not None:
            old_layout = self.left_widget.layout()
            QWidget().setLayout(old_layout)
        self.left_widget.setParent(None)
        self.left_widget = QWidget()
        self.right_widget.setObjectName("left_widget")
        self.splitter.insertWidget(0, self.left_widget)

        self.display_db_tables()

    def display_db_tables(self):
        if self.left_widget.layout() is not None:
            old_layout = self.left_widget.layout()
            QWidget().setLayout(old_layout)

        tree_widget = QTreeWidget()
        tree_widget.setObjectName("customTreeWidget")
        tree_widget.setStyleSheet("border: none;")
        tree_widget.setIndentation(12)
        tree_widget.setHeaderHidden(True)

        tables = [('Basic Configuration',), ('LZB Configuration',), ('MQ Configuration',), ('Communications',),
                  ('NameLists',)]

        for table in tables:
            table_name = table[0]
            table_item = QTreeWidgetItem([table_name])
            table_item.setExpanded(False)
            tree_widget.addTopLevelItem(table_item)

            if table_name == 'Basic Configuration':
                self.basic_config_item = table_item
            elif table_name == 'LZB Configuration':
                self.lzb_config_item = table_item
            elif table_name == 'MQ Configuration':
                self.mq_config_item = table_item
            elif table_name == 'NameLists':
                conn = self.conn_manager.get_db_connection()
                cursor = conn.cursor()
                conn.row_factory = sqlite3.Row
                cursor.execute(f"SELECT id, listName FROM NameList WHERE basicConfig_id = {self.config_manager.config_id};")
                rows = cursor.fetchall()
                self.namelist_item = table_item

                for row in rows:
                    namelist_id = row['id']
                    namelist_name = row['listName']
                    column_item = QTreeWidgetItem([namelist_name])
                    column_item.setData(0, Qt.UserRole, namelist_id)
                    table_item.addChild(column_item)
                conn.close()
            elif table_name == "Communications":
                conn = self.conn_manager.get_db_connection()
                cursor = conn.cursor()
                conn.row_factory = sqlite3.Row
                cursor.execute(f"SELECT id, name FROM Communication WHERE basicConfig_id = {self.config_manager.config_id};")
                rows = cursor.fetchall()
                self.communication_config_item = table_item

                for row in rows:
                    communication_id = row['id']
                    communication_name = row['name']
                    column_item = QTreeWidgetItem([communication_name])
                    column_item.setData(0, Qt.UserRole, communication_id)
                    table_item.addChild(column_item)
                conn.close()

        tree_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        tree_widget.customContextMenuRequested.connect(self.open_context_menu)
        tree_widget.itemClicked.connect(self.on_item_clicked)

        layout = QVBoxLayout()
        layout.addWidget(tree_widget)
        self.left_widget.setLayout(layout)

    def open_context_menu(self, position):
        item = self.left_widget.layout().itemAt(0).widget().itemAt(position)

        if item and item.parent() == self.communication_config_item:
            communication_id = item.data(0, Qt.UserRole)

            menu = QMenu()
            create_new_action = QAction("New Communication", self)
            create_new_action.triggered.connect(lambda: create_new_communication(self))
            menu.addAction(create_new_action)

            delete_action = QAction("Delete selected", self)
            delete_action.triggered.connect(lambda: delete_communication(self, communication_id))
            menu.addAction(delete_action)

            menu.exec_(self.left_widget.layout().itemAt(0).widget().mapToGlobal(position))

        if item and item.parent() == self.namelist_item:
            nameList_id = item.data(0, Qt.UserRole)

            menu = QMenu()
            create_new_action = QAction("New NameList", self)
            create_new_action.triggered.connect(lambda: create_new_namelist(main_window))
            menu.addAction(create_new_action)

            delete_action = QAction("Delete selected", self)
            delete_action.triggered.connect(lambda: delete_selected_namelist(self, nameList_id))
            menu.addAction(delete_action)

            menu.exec_(self.left_widget.layout().itemAt(0).widget().mapToGlobal(position))

    def update_communication_in_tree(self, communication_id, new_name):
        for i in range(self.communication_config_item.childCount()):
            child_item = self.communication_config_item.child(i)
            if child_item.data(0, Qt.UserRole) == communication_id:
                child_item.setText(0, new_name)
                break

    def delete_new_communication(self):
        delete_new_communication(self)

    def delete_selected_communication(self):
        tree_widget = self.left_widget.layout().itemAt(0).widget()
        current_item = tree_widget.currentItem()
        if current_item and current_item.parent() == self.communication_config_item:
            communication_id = current_item.data(0, Qt.UserRole)
            delete_communication(communication_id)

    def delete_selected_namelist(self):
        tree_widget = self.left_widget.layout().itemAt(0).widget()
        current_item = tree_widget.currentItem()
        if current_item and current_item.parent() == self.namelist_item:
            nameList_id = current_item.data(0, Qt.UserRole)
            delete_selected_namelist(self, nameList_id)

    def update_namelist_in_tree(self, nameList_id, new_name):
        for i in range(self.namelist_item.childCount()):
            child_item = self.namelist_item.child(i)
            if child_item.data(0, Qt.UserRole) == nameList_id:
                child_item.setText(0, new_name)
                break

    def on_item_clicked(self, item):
        try:
            communication_id = item.data(0, Qt.UserRole)
            if hasattr(self,
                       'unsaved_changes') and self.unsaved_changes and not self.name_changed and communication_id != self.current_communication_id:
                reply = show_unsaved_changes_warning(self)
                if reply == QMessageBox.No:
                    tree_widget = self.left_widget.layout().itemAt(0).widget()
                    new_comm_items = tree_widget.findItems("New Communication", Qt.MatchExactly | Qt.MatchRecursive)
                    if new_comm_items:
                        tree_widget.setCurrentItem(new_comm_items[0])
                    return
                elif reply == QMessageBox.Yes:
                    self.delete_new_communication()

            if item.parent() == self.communication_config_item:
                if communication_id is not None:
                    self.right_widget.setParent(None)
                    communication_ui = CommunicationUI(communication_id)
                    communication_ui.name_updated.connect(self.update_communication_in_tree)
                    self.right_widget = communication_ui
                    self.right_widget.setObjectName("communications_widget")
                    self.splitter.addWidget(self.right_widget)
                    self.splitter.setSizes([250, 1000])
                    self.setCentralWidget(self.splitter)
                    communication_ui.populate_fields_from_db()
                    self.unsaved_changes = False
                    self.current_communication_id = communication_id
            elif item.parent() == self.namelist_item:
                namelist_id = item.data(0, Qt.UserRole)
                self.load_namelists_view(namelist_id)
            elif item == self.basic_config_item:
                self.load_basic_config_view()
            elif item == self.lzb_config_item:
                self.load_lzb_config_view()
            elif item == self.mq_config_item:
                self.load_mq_config_view()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def load_basic_config_view(self):
        self.right_widget.setParent(None)
        self.right_widget = BasicConfigurationWidget(self)
        self.right_widget.setObjectName("basic_config_widget")
        self.splitter.addWidget(self.right_widget)
        self.splitter.setSizes([250, 1000])

    def load_lzb_config_view(self):
        self.right_widget.setParent(None)
        self.right_widget = LZBConfigurationWidget(self)
        self.right_widget.setObjectName("lzb_config_widget")
        self.splitter.addWidget(self.right_widget)
        self.splitter.setSizes([250, 1000])

    def load_mq_config_view(self):
        self.right_widget.setParent(None)
        self.right_widget = MQConfigurationWidget(self)
        self.right_widget.setObjectName("mq_config_widget")
        self.splitter.addWidget(self.right_widget)
        self.splitter.setSizes([250, 1000])

    def load_namelists_view(self, namelist_id=None):
        self.right_widget.setParent(None)
        if namelist_id is not None:
            self.right_widget = NameListsWidget(nameList_id=namelist_id)
        else:
            self.right_widget = NameListsWidget(self)

        self.right_widget.name_updated.connect(self.update_namelist_in_tree)
        self.right_widget.setObjectName("namelists_widget")
        self.splitter.addWidget(self.right_widget)
        self.splitter.setSizes([250, 1000])

    def save_config(self):
        file_path = self.config_manager.config_filepath
        self._export_to_file(file_path)
        self.update_window_title(file_path)

    def export_config(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save XML File", "", "XML Files (*.xml);;All Files (*)", options=options
        )
        if file_path:
            self._export_to_file(file_path)
            self.update_window_title(file_path)

    def _export_to_file(self, file_path):
        if not self.config_manager or not self.config_manager.config_id:
            QMessageBox.warning(self, "Error", "No configuration loaded. Please load an XML file first.")
            return

        if file_path:
            try:
                export_to_xml_function(file_path, self.config_manager.config_id)
                QMessageBox.information(self, "Success", f"Data saved successfully to:\n{file_path}")
                self.config_manager.config_filepath = file_path
            except Exception:
                QMessageBox.critical(self, "Error", "Failed to export data")
        else:
            QMessageBox.warning(self, "Cancelled", "Export operation was cancelled.")

    def update_window_title(self, file_path):
        #file_name = os.path.basename(file_path)
        self.setWindowTitle(f"{self.app_name} - {file_path}")

    def exit_application(self):
        self.close()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Confirm Exit",
                                     "Are you sure you want to close the application?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.perform_cleanup()
            event.accept()
            QApplication.quit()
        else:
           event.ignore()

    def perform_cleanup(self):
        empty_database()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
