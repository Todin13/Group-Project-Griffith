from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import markdown


class Bubble(QLabel):
    def __init__(self, text, is_user=True):
        super().__init__(text)
        self.setWordWrap(True)
        self.setFont(QFont("Arial", 10))
        self.setMargin(10)
        self.setMaximumWidth(400)
        self.setStyleSheet(
            "QLabel {"
            f"background-color: {"#A52A2A" if is_user else "#808080"};"
            "border-radius: 10px;"
            "padding: 5px;"
            "color: white;"
            "}"
        )
        self.setAlignment(Qt.AlignRight if is_user else Qt.AlignLeft)

        self.set_markdown(text)

    def set_markdown(self, text):
        html = markdown.markdown(text)
        self.setText(html)