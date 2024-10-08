import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QSplitter, QWidget, QVBoxLayout, QTreeWidget, \
    QTreeWidgetItem

from gui.dialog_window import FileDialog
from gui.communication_ui import setup_right_interface

from database.populating_data import data_populating
from database.xml_data_to_db import get_db_connection

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.input_field = None
        self.recent_files = []

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

        export_action = QAction('Export', self)
        file_menu.addAction(export_action)  # TODO: add functionality

        export_as_action = QAction('Export as ...', self)
        file_menu.addAction(export_as_action)  # TODO: add functionality

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

        setup_right_interface(self.right_widget)

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
            table_item = QTreeWidgetItem([table_name])
            tree_widget.addTopLevelItem(table_item)

            if table_name == "Communication":
                cursor.execute(f"SELECT name FROM {table_name};")
                names = cursor.fetchall()

                for name in names:
                    column_item = QTreeWidgetItem([name[0]])
                    table_item.addChild(column_item)

            else:
                cursor.execute(f"PRAGMA table_info({table_name});")
                columns = cursor.fetchall()

                for column in columns:
                    column_name = column[1]
                    column_item = QTreeWidgetItem([column_name])
                    table_item.addChild(column_item)

            table_item.setExpanded(False)

        tree_widget.itemClicked.connect(self.on_item_clicked)

        layout = QVBoxLayout()
        layout.addWidget(tree_widget)
        self.left_widget.setLayout(layout)

    def on_item_clicked(self, item, column):
        parent = item.parent()
        if parent and parent.text(0) == "Communication":
            name = item.text(0)
            data_populating(name)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    with open("styles.css", "r", encoding="utf-8") as f:
        css = f.read()
        app.setStyleSheet(css)

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())