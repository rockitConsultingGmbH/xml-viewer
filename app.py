import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QSplitter, QWidget

from gui.dialog_window import FileDialog


# Settings for the main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(1280, 720)
        self.setWindowTitle("XML Editor")

        screen = QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        open_xml_action = QAction('Open XML', self)
        open_xml_action.triggered.connect(self.open_xml)
        file_menu.addAction(open_xml_action)

        splitter = QSplitter(Qt.Horizontal)

        left_widget = QWidget()
        right_widget = QWidget()

        left_widget.setStyleSheet("background-color: white; border: 1px solid #A9A9A9;")
        right_widget.setStyleSheet("background-color: white; border: 1px solid #A9A9A9;")

        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)

        splitter.setSizes([300, 980])

        self.setCentralWidget(splitter)

#Function to open the XML file
    def open_xml(self):
        dialog = FileDialog(self)
        if dialog.exec_():
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())