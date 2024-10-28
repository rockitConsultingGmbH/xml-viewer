import sqlite3
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QSplitter, QWidget, QVBoxLayout, QTreeWidget, \
    QTreeWidgetItem, QMessageBox, QFileDialog

from utils.empty_database import empty_database
from gui.import_xml_dialog_window import FileDialog
from gui.communication_ui import CommunicationUI
from gui.basic_configuration_ui import BasicConfigurationWidget
from gui.lzb_configuration_ui import LZBConfigurationWidget
from gui.mq_configuration_ui import MQConfigurationWidget

from common.connection_manager import ConnectionManager

from gui.namelists_ui import NameListsWidget
from utils.export_db_to_xml.db_to_xml import export_to_xml as export_to_xml_function
from common import config_manager

from gui.common_components.stylesheet_loader import load_stylesheet


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.input_field = None
        self.recent_files = []
        self.basic_config_item = None
        self.conn_manager = ConnectionManager().get_instance()

        self.resize(1800, 900)
        self.setWindowTitle("XML Editor")

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

        selection_menu = menubar.addMenu('Selection')

        copy_action = QAction('Copy', self)
        selection_menu.addAction(copy_action)

        delete_action = QAction('Delete', self)
        selection_menu.addAction(delete_action)


    def open_xml(self):
        dialog = FileDialog(self)
        if dialog.exec_():
            if self.recent_files:
                self.reinitialize()
            self.display_db_tables()

            # Automatically display the Basic Configuration view after loading the XML
            self.load_basic_config_view()

            # Select the Basic Configuration item in the left tree widget
            if self.basic_config_item:
                tree_widget = self.left_widget.layout().itemAt(0).widget()
                tree_widget.setCurrentItem(self.basic_config_item)

    def reinitialize(self):
        """Reinitialize the application state for a new XML import."""

        # Remove layout and widgets for right_widget
        if self.right_widget.layout() is not None:
            old_layout = self.right_widget.layout()
            QWidget().setLayout(old_layout)  # Detach and delete the old layout
        self.right_widget.setParent(None)
        self.right_widget = QWidget()
        self.right_widget.setObjectName("right_widget")
        self.splitter.addWidget(self.right_widget)

        # Remove layout and widgets for left_widget
        if self.left_widget.layout() is not None:
            old_layout = self.left_widget.layout()
            QWidget().setLayout(old_layout)  # Detach and delete the old layout
        self.left_widget.setParent(None)
        self.left_widget = QWidget()
        self.right_widget.setObjectName("left_widget")
        self.splitter.insertWidget(0, self.left_widget)

        # Call method to re-display the tables
        self.display_db_tables()

    def display_db_tables(self):
        # Check if the left widget already has a layout and clear it
        if self.left_widget.layout() is not None:
            old_layout = self.left_widget.layout()
            QWidget().setLayout(old_layout)  # Detach and delete the old layout

        # Initialize a new QTreeWidget
        tree_widget = QTreeWidget()
        tree_widget.setObjectName("customTreeWidget")
        tree_widget.setStyleSheet("border: none;")
        tree_widget.setIndentation(0)
        tree_widget.setHeaderHidden(True)

        # Define tables with titles
        tables = [('Basic Configuration',), ('LZB Configuration',), ('MQ Configuration',), ('Communications',),
                  ('NameLists',)]

        for table in tables:
            table_name = table[0]
            table_item = QTreeWidgetItem([table_name])

            # Ensure each item is collapsed by default
            table_item.setExpanded(False)

            tree_widget.addTopLevelItem(table_item)

            if table_name == 'Basic Configuration':
                self.basic_config_item = table_item
            elif table_name == 'LZB Configuration':
                self.lzb_config_item = table_item
            elif table_name == 'MQ Configuration':
                self.mq_config_item = table_item
            elif table_name == 'NameLists':
                # self.namelists_item = table_item

                conn = self.conn_manager.get_db_connection()
                cursor = conn.cursor()
                conn.row_factory = sqlite3.Row
                cursor.execute(f"SELECT id, listName FROM NameList WHERE basicConfig_id = {config_manager.config_id};")
                rows = cursor.fetchall()
                self.namelist_item = table_item

                # Add child items to 'Communications'
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
                cursor.execute(f"SELECT id, name FROM Communication WHERE basicConfig_id = {config_manager.config_id};")
                rows = cursor.fetchall()
                self.communication_config_item = table_item

                # Add child items to 'Communications'
                for row in rows:
                    communication_id = row['id']
                    communication_name = row['name']

                    column_item = QTreeWidgetItem([communication_name])
                    column_item.setData(0, Qt.UserRole, communication_id)
                    table_item.addChild(column_item)
                conn.close()

        tree_widget.itemClicked.connect(self.on_item_clicked)

        # Set layout with the updated tree widget
        layout = QVBoxLayout()
        layout.addWidget(tree_widget)
        self.left_widget.setLayout(layout)

    def on_item_clicked(self, item):
        if item.parent() == self.communication_config_item:
            communication_id = item.data(0, Qt.UserRole)
            if communication_id is not None:
                print(f"Communication ID: {communication_id}")
                self.right_widget.setParent(None)
                communication_ui = CommunicationUI(communication_id)
                self.right_widget = communication_ui
                self.right_widget.setObjectName("communications_widget")
                self.splitter.addWidget(self.right_widget)
                self.splitter.setSizes([250, 1000])
                self.setCentralWidget(self.splitter)

                communication_ui.populate_fields_from_db()

        elif item == self.basic_config_item:
            self.load_basic_config_view()
        elif item == self.lzb_config_item:
            self.load_lzb_config_view()
        elif item == self.mq_config_item:
            self.load_mq_config_view()
        elif item.parent() == self.namelist_item:
            namelist_id = item.data(0, Qt.UserRole)
            print(f"NameList ID: {namelist_id}")
            self.load_namelists_view(namelist_id)

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

        # Connect the name_updated signal to the slot that updates the name in the tree
        self.right_widget.name_updated.connect(self.update_namelist_in_tree)
        self.right_widget.setObjectName("namelists_widget")
        self.splitter.addWidget(self.right_widget)
        self.splitter.setSizes([250, 1000])

    def update_namelist_in_tree(self, nameList_id, new_name):
        """Update the NameList name in the tree widget when it is changed."""
        for i in range(self.namelist_item.childCount()):
            child_item = self.namelist_item.child(i)
            if child_item.data(0, Qt.UserRole) == nameList_id:
                # Update the name in the tree widget
                child_item.setText(0, new_name)
                break

    def save_config(self):
        """Save configuration to a predetermined file path."""
        file_path = config_manager.config_filepath
        self._export_to_file(file_path)
        self.update_window_title(file_path)

    def export_config(self):
        """Export configuration with a user-specified file path."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save XML File", "", "XML Files (*.xml);;All Files (*)", options=options
        )
        if file_path:
            self._export_to_file(file_path)
            self.update_window_title(file_path)

    def _export_to_file(self, file_path):
        """Handles file export operations for configuration data."""
        if not config_manager or not config_manager.config_id:
            QMessageBox.warning(self, "Error", "No configuration loaded. Please load an XML file first.")
            return

        if file_path:
            try:
                export_to_xml_function(file_path, config_manager.config_id)
                QMessageBox.information(self, "Success", f"Data saved successfully to:\n{file_path}")
                config_manager.config_filepath = file_path
            except Exception:
                QMessageBox.critical(self, "Error", "Failed to export data")
        else:
            QMessageBox.warning(self, "Cancelled", "Export operation was cancelled.")

    def update_window_title(self, file_path):
        """Update the window title with the file name."""
        #file_name = os.path.basename(file_path)
        self.setWindowTitle(f"XML Editor - {file_path}")

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
