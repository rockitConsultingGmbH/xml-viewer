import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QSplitter, QTreeWidget, QTreeWidgetItem,
    QAction, QFileDialog
)
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("XML Editor")
        self.resize(1600, 900)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        open_action = QAction("Open XML File", self)
        open_action.triggered.connect(self.open_xml_file)
        file_menu.addAction(open_action)

        splitter = QSplitter(self)
        splitter.setOrientation(Qt.Horizontal)

        self.table_tree = QTreeWidget()
        self.table_tree.header().hide()
        self.table_tree.itemExpanded.connect(self.load_columns)
        self.table_tree.setFixedWidth(400)

        splitter.addWidget(self.table_tree)
        self.setCentralWidget(splitter)

        self.load_tables()

    def load_tables(self):
        self.table_tree.clear()
        tables = self.database.fetch_tables()
        for table in tables:
            table_item = QTreeWidgetItem(self.table_tree, [table])
            table_item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
            table_item.setExpanded(False)

    def load_columns(self, item):
        if item.childCount() == 0:
            table_name = item.text(0)
            if table_name == "Communication":
                communication_names = self.database.fetch_communication_names()
                for name in communication_names:
                    name_item = QTreeWidgetItem(item, [name])
                    name_item.setChildIndicatorPolicy(QTreeWidgetItem.DontShowIndicator)
            else:
                columns = self.database.fetch_columns(table_name)
                for column in columns:
                    column_item = QTreeWidgetItem(item, [column])
                    column_item.setChildIndicatorPolicy(QTreeWidgetItem.DontShowIndicator)

    def open_xml_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Choose your XML File", "", "XML Files (*.xml)", options=options)
        if file_name:
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())