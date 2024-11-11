from PyQt5.QtWidgets import QApplication, QLineEdit, QCheckBox, QLabel
from PyQt5.QtCore import Qt

def get_input_value(widget_name):
    widget = next((widget for widget in QApplication.allWidgets() if
                   isinstance(widget, QLineEdit) and widget.objectName() == widget_name), None)
    return widget.text() if widget else ""

def set_input_value(widget_name, value):
    widget = next((widget for widget in QApplication.allWidgets() if
                   isinstance(widget, QLineEdit) and widget.objectName() == widget_name), None)
    if widget:
        widget.blockSignals(True)
        widget.setText(value or "")
        widget.blockSignals(False)

def set_checkbox_value(widget_name, value):
    checkbox = next((widget for widget in QApplication.allWidgets() if
                     isinstance(widget, QCheckBox) and widget.objectName() == widget_name), None)
    if checkbox:
        checkbox.blockSignals(True)
        checkbox.setChecked(value in [1, '1', True, 'true'])
        checkbox.blockSignals(False)

def get_checkbox_value(widget_name):
    checkbox = next((widget for widget in QApplication.allWidgets() if
                     isinstance(widget, QCheckBox) and widget.objectName() == widget_name), None)
    return checkbox.isChecked() if checkbox else False

def convert_checkbox_to_string(checkbox_value):
    return "true" if checkbox_value else "false"

def set_text_field(parent_widget, field_name, value):
    text_field = parent_widget.findChild(QLineEdit, field_name)
    if value:
        if text_field:
            text_field.setText(value)
    else:
        text_field.setText("")

def set_checkbox_field(parent_widget, field_name, value):
    if value:
        checkbox = parent_widget.findChild(QCheckBox, field_name)
        if checkbox:
            checkbox.setChecked(value.lower() == 'true')

def set_label(parent_widget, field_name, value):
    text_field = parent_widget.findChild(QLabel, field_name)
    if value:
        if text_field:
            text_field.setText(value)
    else:
        text_field.setText("")

def get_text_value(parent_widget, widget_name):
    widget = parent_widget.findChild(QLineEdit, widget_name, Qt.FindChildrenRecursively)
    if widget:
        return widget.text()
    else:
        return ""

def get_checkbox_value(parent_widget, widget_name):
    widget = parent_widget.findChild(QCheckBox, widget_name, Qt.FindChildrenRecursively)
    if widget:
        return widget.isChecked()
    else:
        return False