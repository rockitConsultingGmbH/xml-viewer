from PyQt5.QtWidgets import (QHBoxLayout, QPushButton)

def create_button_layout(self):
    button_layout = QHBoxLayout()
    button_layout.addStretch()

    reset_button = QPushButton("Reset")
    reset_button.setFixedSize(100, 30)
    reset_button.setStyleSheet("background-color: #960e0e; color: white;")
    reset_button.clicked.connect(self.populate_fields_from_db)

    save_button = QPushButton("Save")
    save_button.setFixedSize(100, 30)
    save_button.setStyleSheet("background-color: #41414a; color: white;")
    save_button.clicked.connect(self.save_fields_to_db)

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