from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel


class ClickableLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)