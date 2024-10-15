import sqlite3
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QSplitter, QWidget, QVBoxLayout, QTreeWidget, \
    QTreeWidgetItem, QMessageBox, QFileDialog

from controllers.empty_database import empty_database
from gui.import_xml_dialog_window import FileDialog
from gui.communication_ui import setup_right_interface
from gui.basic_configuration_ui import BasicConfigurationWidget
from gui.lzb_configuration_ui import LZBConfigurationWidget

from common.connection_manager import ConnectionManager
from controllers.communication_table_data import populate_communication_table_fields
from controllers.location_table_data import populate_location_table_fields
from controllers.description_table_data import populate_description_fields
from common.connection_manager import ConnectionManager
from gui.mq_configuration_ui import MQConfigurationWidget

from utils.export_db_to_xml.db_to_xml import export_to_xml as export_to_xml_function
from common import config_manager

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

        export_action = QAction('Saves As...', self)
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

        communication_menu = menubar.addMenu('Communication')

        copy_action = QAction('Copy', self)
        communication_menu.addAction(copy_action)  # TODO: add functionality

        delete_action = QAction('Delete', self)
        communication_menu.addAction(delete_action)  # TODO: add functionality

        self.splitter = QSplitter(Qt.Horizontal)

        self.left_widget = QWidget()
        self.right_widget = QWidget()

        self.left_widget.setStyleSheet("background-color: white; border: 1px solid #A9A9A9;")
        self.right_widget.setStyleSheet("background-color: white; border: 1px solid #A9A9A9;")

        self.splitter.addWidget(self.left_widget)
        self.splitter.addWidget(self.right_widget)

        self.splitter.setSizes([250, 1000])

        self.setCentralWidget(self.splitter)

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
        self.right_widget.setStyleSheet("background-color: white; border: 1px solid #A9A9A9;")
        self.splitter.addWidget(self.right_widget)

        # Remove layout and widgets for left_widget
        if self.left_widget.layout() is not None:
            old_layout = self.left_widget.layout()
            QWidget().setLayout(old_layout)  # Detach and delete the old layout
        self.left_widget.setParent(None)
        self.left_widget = QWidget()
        self.left_widget.setStyleSheet("background-color: white; border: 1px solid #A9A9A9;")
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
        tree_widget.setStyleSheet("""
            QTreeWidget {
                border: none;
                outline: 0;
                background-color: white;
            }
            QTreeWidget::item {
                font-size: 16px;  
                padding: 10px;    
            }
            QTreeWidget::item:has-children {
                border: 1px solid black; 
            }
            QTreeWidget::item:!has-children {
                border: none;  
                padding-left: 20px; 
            }
            QTreeWidget::item:hover {
                background-color: lightgray;
            }
            QTreeWidget::item:selected {
                background-color: #83acf7;  
            }
        """)

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
            
            # Associate items for later use
            if table_name == 'Basic Configuration':
                self.basic_config_item = table_item
            elif table_name == 'LZB Configuration':
                self.lzb_config_item = table_item
            elif table_name == 'MQ Configuration':
                self.mq_config_item = table_item
            elif table_name == 'Communications':
                # Load data for the Communications section
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

        tree_widget.itemClicked.connect(self.on_item_clicked)

        # Set layout with the updated tree widget
        layout = QVBoxLayout()
        layout.addWidget(tree_widget)
        self.left_widget.setLayout(layout)

    def on_item_clicked(self, item, column):
        if item.parent() == self.communication_config_item:
            communication_id = item.data(0, Qt.UserRole)
            if communication_id is not None:

                self.right_widget.setParent(None)
                self.right_widget = QWidget()
                self.right_widget.setStyleSheet("background-color: white; border: 1px solid #A9A9A9;")
                self.splitter.addWidget(self.right_widget)
                self.splitter.setSizes([250, 1000])
                self.setCentralWidget(self.splitter)

                setup_right_interface(self.right_widget, communication_id)

                populate_communication_table_fields(communication_id)
                populate_location_table_fields(communication_id)
                populate_description_fields(communication_id)

        elif item == self.basic_config_item:
            self.load_basic_config_view()
        elif item == self.lzb_config_item:
            self.load_lzb_config_view()
        elif item == self.mq_config_item:
            self.load_mq_config_view()

    def load_basic_config_view(self):
        self.right_widget.setParent(None)
        self.right_widget = BasicConfigurationWidget(self)
        self.right_widget.setStyleSheet("font-weight: bold; font-size: 15px; border: none;")
        self.right_widget.setStyleSheet("""QLabel {font-weight: bold;}QLineEdit {font-weight: normal;}""")
        self.splitter.addWidget(self.right_widget)
        self.splitter.setSizes([250, 1000])

    def load_lzb_config_view(self):
        self.right_widget.setParent(None)
        self.right_widget = LZBConfigurationWidget(self)
        self.right_widget.setStyleSheet("font-weight: bold; font-size: 15px; border: none;")
        self.right_widget.setStyleSheet("""QLabel {font-weight: bold;}QLineEdit {font-weight: normal;}""")
        self.splitter.addWidget(self.right_widget)
        self.splitter.setSizes([250, 1000])

    def load_mq_config_view(self):
        self.right_widget.setParent(None)
        self.right_widget = MQConfigurationWidget(self)
        self.right_widget.setStyleSheet("font-weight: bold; font-size: 15px; border: none;")
        self.right_widget.setStyleSheet("""QLabel {font-weight: bold;}QLineEdit {font-weight: normal;}""")
        self.splitter.addWidget(self.right_widget)
        self.splitter.setSizes([250, 1000])

    def save_config(self):
        """Save configuration to a predetermined file path."""
        file_path = config_manager.config_filepath
        self._export_to_file(file_path)

    def export_config(self):
        """Export configuration with a user-specified file path."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save XML File", "", "XML Files (*.xml);;All Files (*)", options=options
        )
        self._export_to_file(file_path)

    def _export_to_file(self, file_path):
        """Handles file export operations for configuration data."""
        if not config_manager or not config_manager.config_id:
            QMessageBox.warning(self, "Error", "No configuration loaded. Please load an XML file first.")
            return

        if file_path:
            try:
                export_to_xml_function(file_path, config_manager.config_id)
                QMessageBox.information(self, "Success", f"Data saved successfully to:\n{file_path}")
            except Exception:
                QMessageBox.critical(self, "Error", "Failed to export data")
        else:
            QMessageBox.warning(self, "Cancelled", "Export operation was cancelled.")

    def exit_application(self):
        self.close()
        QApplication.quit()

    # override the closeEvent method to prompt the user before closing the application
    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Confirm Exit",
                                     "Are you sure you want to close the application?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.perform_cleanup()
            event.accept()
        else:
            event.ignore()

    def perform_cleanup(self):
         empty_database()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)

    with open("styles.css", "r", encoding="utf-8") as f:
        css = f.read()
        app.setStyleSheet(css)

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())