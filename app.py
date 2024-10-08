import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QSplitter, QWidget, QVBoxLayout, QTreeWidget, \
    QTreeWidgetItem, QMessageBox, QFileDialog

from gui.dialog_window import FileDialog
from gui.communication_ui import setup_right_interface
from gui.basic_configuration_ui import BasicConfigurationWidget
from gui.lzb_configuration_ui import LZBConfigurationWidget
from database.populating_data import data_populating
from database.xml_to_db import get_db_connection
from gui.mq_configuration_ui import MQConfigurationWidget

from database.db_to_xml import export_to_xml as export_to_xml_function
from common import config_manager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.input_field = None
        self.recent_files = []
        self.basic_config_item = None

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

        save_action = QAction('Save changes', self)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('Ctrl+S')
        file_menu.addAction(save_action)  # TODO: add functionality

        reset_action = QAction('Reset', self)
        reset_action.setShortcut('Ctrl+R')
        reset_action.setStatusTip('Ctrl+R')
        file_menu.addAction(reset_action)  # TODO: add functionality

        export_action = QAction('Export', self)
        export_action.setShortcut('Ctrl+E')
        export_action.setStatusTip('Ctrl+E')
        file_menu.addAction(export_action)
        export_action.triggered.connect(self.export_config)

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

        #setup_right_interface(self.right_widget)

    def open_xml(self):
        dialog = FileDialog(self)
        if dialog.exec_():
            self.display_db_tables()

    def display_db_tables(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

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

        for table in tables:
            table_name = table[0]
            if table_name in ('BasicConfig', 'LzbConfig', 'MqConfig', 'Communication', 'NameList'):
                table_item = QTreeWidgetItem([table_name])
                tree_widget.addTopLevelItem(table_item)

            if table_name == "Communication":
                cursor.execute(f"SELECT name FROM {table_name};")
                names = cursor.fetchall()
                self.communication_config_item = table_item

                for name in names:
                    column_item = QTreeWidgetItem([name[0]])
                    table_item.addChild(column_item)

            if table_name == "BasicConfig":
                table_item.setExpanded(False)
                self.basic_config_item = table_item

            if table_name == "LzbConfig":
                table_item.setExpanded(False)
                self.lzb_config_item = table_item


            if table_name == "MqConfig":
                table_item.setExpanded(False)
                self.mq_config_item = table_item

        tree_widget.itemClicked.connect(self.on_item_clicked)

        layout = QVBoxLayout()
        layout.addWidget(tree_widget)
        self.left_widget.setLayout(layout)

    def on_item_clicked(self, item, column):
        #parent = item.parent()
        if item.parent() == self.communication_config_item:
            self.right_widget.setParent(None)
            #self.left_widget = QWidget()
            self.right_widget = QWidget()
            #self.left_widget.setStyleSheet("background-color: white; border: 1px solid #A9A9A9;")
            self.right_widget.setStyleSheet("background-color: white; border: 1px solid #A9A9A9;")
            #self.splitter.addWidget(self.left_widget)
            self.splitter.addWidget(self.right_widget)
            self.splitter.setSizes([250, 1000])
            self.setCentralWidget(self.splitter)
            setup_right_interface(self.right_widget)
            name = item.text(0)
            data_populating(name)
        if item == self.basic_config_item:
            self.load_basic_config_view()
        if item == self.lzb_config_item:
            self.load_lzb_config_view()
        if item == self.mq_config_item:
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

    def export_config(self):
        try:
            if config_manager is None or not config_manager.config_id:
                QMessageBox.warning(self, "Error", "No configuration loaded. Please load an XML file first.")
                return

            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self, "Save XML File", "", "XML Files (*.xml);;All Files (*)", options=options)

            if file_path:
                export_to_xml_function(file_path, config_manager.config_id)
                QMessageBox.information(self, "Success", "Data exported to XML successfully.")
            else:
                QMessageBox.warning(self, "Cancelled", "Export operation was cancelled.")
        except Exception as e:
            #QMessageBox.critical(self, "Error", f"Failed to export data: {e}")
            QMessageBox.critical(self, "Error", f"Failed to export data")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    with open("styles.css", "r", encoding="utf-8") as f:
        css = f.read()
        app.setStyleSheet(css)

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())