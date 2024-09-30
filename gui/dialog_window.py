from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit, QHBoxLayout, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon
from database.xml_data_to_db import validate_xml, insert_data_into_db


class FileDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Choose XML and XSD Files")
        self.setGeometry(100, 100, 400, 200)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self.setWindowIcon(QIcon('gui/icon/pick_file.svg'))

        layout = QVBoxLayout()

        self.xml_label = QLabel("Choose XML File:")
        self.xml_path = QLineEdit()
        self.xml_path.setReadOnly(True)
        self.xml_button = QPushButton()
        self.xml_button.setIcon(QIcon('gui/icon/folder.svg'))
        self.xml_button.clicked.connect(self.choose_xml_file)
        xml_layout = QHBoxLayout()
        xml_layout.addWidget(self.xml_path)
        xml_layout.addWidget(self.xml_button)

        self.xsd_label = QLabel("Choose XSD Schema:")
        self.xsd_path = QLineEdit()
        self.xsd_path.setReadOnly(True)
        self.xsd_button = QPushButton()
        self.xsd_button.setIcon(QIcon('gui/icon/folder.svg'))
        self.xsd_button.clicked.connect(self.choose_xsd_file)
        xsd_layout = QHBoxLayout()
        xsd_layout.addWidget(self.xsd_path)
        xsd_layout.addWidget(self.xsd_button)

        self.validate_button = QPushButton("Validate and continue")
        self.validate_button.clicked.connect(self.validate_and_continue)

        layout.addWidget(self.xml_label)
        layout.addLayout(xml_layout)
        layout.addWidget(self.xsd_label)
        layout.addLayout(xsd_layout)
        layout.addWidget(self.validate_button)

        self.setLayout(layout)

    def choose_xml_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Choose XML File", "", "XML Files (*.xml);;All Files (*)")
        if file_name:
            self.xml_path.setText(file_name)

    def choose_xsd_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Choose XSD Schema", "", "XSD Files (*.xsd)")
        if file_name:
            self.xsd_path.setText(file_name)

    def validate_and_continue(self):
        xml_file = self.xml_path.text()
        xsd_file = self.xsd_path.text()

        if xml_file and xsd_file:
            try:
                xml_tree = validate_xml(xml_file, xsd_file)
                insert_data_into_db(xml_tree, self.xml_path.text())
                QMessageBox.information(self, "Success", "XML file was successfully opened and validated.")
                self.accept()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error: {str(e)}")

    def showEvent(self, event):
        super().showEvent(event)
        parent_geometry = self.parent().geometry()
        self.move(
            parent_geometry.center().x() - self.width() // 2,
            parent_geometry.center().y() - self.height() // 2
        )
