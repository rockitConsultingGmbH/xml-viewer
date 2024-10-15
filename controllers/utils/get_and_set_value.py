from PyQt5.QtWidgets import QApplication, QLineEdit, QCheckBox


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