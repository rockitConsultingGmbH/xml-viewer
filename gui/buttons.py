from PyQt5.QtWidgets import (QHBoxLayout, QPushButton)

BUTTON_STYLE = "background-color: {}; color: white;"
BUTTON_SIZE = (100, 30)

class ButtonFactory:
    def __init__(self):
        pass

    def create_button_layout(self, parent):
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        reset_button = self.create_button("Reset", "#960e0e", parent.set_fields_from_db)
        save_button = self.create_button("Save", "#41414a", parent.save_fields_to_db)

        button_layout.addWidget(reset_button)
        button_layout.addWidget(save_button)
            
        return button_layout

    def create_button(self, label, color, callback):
        """Helper function to create a styled button with a callback."""
        button = QPushButton(label)
        button.setFixedSize(*BUTTON_SIZE)
        button.setStyleSheet(BUTTON_STYLE.format(color))
        button.clicked.connect(callback)
        return button