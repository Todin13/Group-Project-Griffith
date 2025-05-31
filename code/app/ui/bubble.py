from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

def create_chat_bubble(text, is_user=True, bot_name="GriffithAI"):
    bubble = QLabel(text)
    bubble.setObjectName("chat_text")
    bubble.setWordWrap(True)
    bubble.setFont(QFont("Arial", 11))
    bubble.setTextInteractionFlags(Qt.TextSelectableByMouse)
    bubble.setStyleSheet(f"""
        QLabel {{
            background-color: {"#A52A2A" if is_user else "#808080"};
            color: {'white'};
            border-radius: 15px;
            padding: 12px;
        }}
    """)

    layout = QVBoxLayout()
    layout.setContentsMargins(10, 5, 10, 5)

    if not is_user:
        name_label = QLabel(bot_name)
        name_label.setFont(QFont("Arial", 9, QFont.Bold))
        name_label.setStyleSheet("color: #444; margin-left: 6px;")
        layout.addWidget(name_label, alignment=Qt.AlignLeft)

    layout.addWidget(bubble, alignment=Qt.AlignRight if is_user else Qt.AlignLeft)

    container = QWidget()
    container.setLayout(layout)
    return container