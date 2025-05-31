from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont

def create_top_bar(bot_name="GriffAI"):
    top_bar = QWidget()
    layout = QHBoxLayout()
    layout.setContentsMargins(10, 10, 10, 10)
    layout.setSpacing(8)
    
    # Icon label
    icon_label = QLabel()
    pixmap = QPixmap("app/resources/chatbot.png").scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    icon_label.setPixmap(pixmap)
    
    # Text label
    text_label = QLabel(bot_name)
    text_label.setFont(QFont("Arial", 16, QFont.Bold))
    text_label.setAlignment(Qt.AlignCenter)
    
    layout.addWidget(icon_label)
    layout.addWidget(text_label)
    layout.setAlignment(Qt.AlignCenter)
    
    top_bar.setLayout(layout)
    top_bar.setStyleSheet("background-color: #A52A2A;color: white")
    
    return top_bar
