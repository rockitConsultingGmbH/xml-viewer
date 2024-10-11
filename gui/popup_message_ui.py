from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtCore import Qt, QTimer

class PopupMessage:
    def __init__(self, parent: QWidget, max_width: int = 800, height: int = 30, duration: int = 3000):
        self.parent = parent
        self.duration = duration
        self.max_width = max_width  # Maximum width to prevent oversized messages

        # Create the bubble popup message label
        self.popup_message = QLabel(parent)
        self.popup_message.setStyleSheet("""
            background-color: lightgreen; 
            color: black; 
            padding: 5px 10px; 
            border-radius: 10px; 
            border: 1px solid green;
        """)
        self.popup_message.setAlignment(Qt.AlignCenter)
        self.popup_message.setFixedHeight(height)
        self.popup_message.setVisible(False)  # Initially hidden

        # Initialize the timer to control the visibility of the popup message
        self.message_timer = QTimer()
        self.message_timer.setSingleShot(True)
        self.message_timer.timeout.connect(self.hide_success_message)

    def show_message(self, text: str):
        # Set the message text and adjust the width
        self.popup_message.setText(text)
        # Set the width based on text length, with a limit on the maximum width
        text_width = self.popup_message.fontMetrics().boundingRect(text).width() + 50
        adjusted_width = min(self.max_width, text_width)
        self.popup_message.setFixedWidth(adjusted_width)

        # Position the popup centered horizontally, adjust vertical positioning if needed
        top_margin = 20  # adjust as needed for spacing
        self.popup_message.move((self.parent.width() - self.popup_message.width()) // 2, top_margin)
        self.popup_message.setVisible(True)

        # Start the timer to hide the message after the specified duration
        self.message_timer.start(self.duration)

    def hide_success_message(self):
        self.popup_message.setVisible(False)
