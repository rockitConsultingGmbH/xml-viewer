from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtCore import Qt, QTimer


class PopupMessage:
    def __init__(self, parent: QWidget, max_width: int = 800, height: int = 30, duration: int = 3000):
        self.parent = parent
        self.duration = duration
        self.max_width = max_width

        self.popup_message = QLabel(parent)
        self.popup_message.setAlignment(Qt.AlignCenter)
        self.popup_message.setFixedHeight(height)
        self.popup_message.setVisible(False)

        self.message_timer = QTimer()
        self.message_timer.setSingleShot(True)
        self.message_timer.timeout.connect(self.hide_success_message)

    def show_message(self, text: str):
        self.popup_message.setStyleSheet("""
            background-color: lightblue; 
            color: black; 
            padding: 5px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: bold;
        """)
        self.popup_message.setText(text)
        text_width = self.popup_message.fontMetrics().boundingRect(text).width() + 50
        adjusted_width = min(self.max_width, text_width)
        self.popup_message.setFixedWidth(adjusted_width)

        top_margin = 10
        self.popup_message.move((self.parent.width() - self.popup_message.width()) // 2, top_margin)
        self.popup_message.setVisible(True)

        self.message_timer.start(self.duration)

    def show_error_message(self, text: str):
        self.show_message(text)
        self.popup_message.setStyleSheet("""
            background-color: orange; 
            color: black; 
            padding: 5px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: bold;
        """)

    def hide_success_message(self):
        self.popup_message.setVisible(False)
