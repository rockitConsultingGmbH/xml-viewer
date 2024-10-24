from PyQt5.QtWidgets import QLabel, QHBoxLayout, QFormLayout

def delete_field(form_layout, label_should_be_deleted: QLabel, hbox_layout: QHBoxLayout):
    form_layout.removeWidget(label_should_be_deleted)
    form_layout.removeItem(hbox_layout)

    label_should_be_deleted.deleteLater()
    for i in range(hbox_layout.count()):
        widget = hbox_layout.itemAt(i).widget()
        if widget:
            widget.deleteLater()

    hbox_layout.deleteLater()

def delete_all_fields(form_layouts: list):
    for layout in form_layouts:
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            if item.widget():
                widget = item.widget()
                widget.deleteLater()
            else:
                layout.removeItem(item)



