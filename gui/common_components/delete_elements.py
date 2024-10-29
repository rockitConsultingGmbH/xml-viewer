from PyQt5.QtWidgets import QLabel, QHBoxLayout, QWidget

def delete_field(form_layout, label_should_be_deleted: QLabel, hbox_layout: QHBoxLayout):
    form_layout.removeWidget(label_should_be_deleted)
    form_layout.removeItem(hbox_layout)

    label_should_be_deleted.deleteLater()
    for i in range(hbox_layout.count()):
        widget = hbox_layout.itemAt(i).widget()
        if widget:
            widget.deleteLater()

    hbox_layout.deleteLater()

def delete_all_fields(widget: QWidget):
    parent_layout = widget.parentWidget().layout()
    parent_layout.removeWidget(widget)
    widget.deleteLater()


