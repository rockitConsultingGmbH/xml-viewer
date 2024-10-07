from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit, QHBoxLayout, QFileDialog, QMessageBox, QCheckBox
from PyQt5.QtGui import QIcon
from lxml import etree  # Не забудьте добавить lxml
from database.xml_data_to_db import validate_xml, insert_data_into_db
from common import config_manager

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

        # Добавляем чекбокс для активации валидации
        self.validate_checkbox = QCheckBox("Validate XML against XSD")
        self.validate_checkbox.setChecked(False)  # Установить по умолчанию в false
        self.validate_checkbox.toggled.connect(self.toggle_xsd_fields)  # Подключаем метод к событию

        self.validate_button = QPushButton("Open and continue")
        self.validate_button.clicked.connect(self.validate_and_continue)

        layout.addWidget(self.xml_label)
        layout.addLayout(xml_layout)
        layout.addWidget(self.xsd_label)
        layout.addLayout(xsd_layout)
        layout.addWidget(self.validate_checkbox)
        layout.addWidget(self.validate_button)

        self.setLayout(layout)

        # Устанавливаем состояние полей XSD при инициализации
        self.toggle_xsd_fields()

    def choose_xml_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Choose XML File", "", "XML Files (*.xml);;All Files (*)")
        if file_name:
            self.xml_path.setText(file_name)

    def choose_xsd_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Choose XSD Schema", "", "XSD Files (*.xsd)")
        if file_name:
            self.xsd_path.setText(file_name)

    def toggle_xsd_fields(self):
        # Включаем или отключаем поля выбора XSD в зависимости от состояния чекбокса
        is_checked = self.validate_checkbox.isChecked()
        self.xsd_path.setEnabled(is_checked)
        self.xsd_button.setEnabled(is_checked)

    def validate_and_continue(self):
        xml_file = self.xml_path.text()
        xsd_file = self.xsd_path.text() if self.validate_checkbox.isChecked() else None

        if xml_file:
            if self.validate_checkbox.isChecked() and not xsd_file:
                QMessageBox.warning(self, "Warning", "Please select an XSD schema for validation.")
                return

            try:
                xml_tree = None
                if self.validate_checkbox.isChecked() and xsd_file:
                    xml_tree = validate_xml(xml_file, xsd_file)
                else:
                    with open(xml_file, 'rb') as file:
                        xml_tree = etree.parse(file)

                config_manager.config_id = insert_data_into_db(xml_tree, self.xml_path.text())
                QMessageBox.information(self, "Success", "XML file was successfully opened.")
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
