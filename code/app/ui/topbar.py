from PyQt5.QtWidgets import  QWidget, QLabel, QHBoxLayout, QPushButton, QMenu, QAction

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from app.ui.terms_dialog import TermsDialog  

def create_top_bar(bot_name="GriffAI", parent=None):
    top_bar = QWidget()
    layout = QHBoxLayout()
    layout.setContentsMargins(10, 10, 10, 10)
    layout.setSpacing(8)

    # Icon
    icon_label = QLabel()
    pixmap = QPixmap("app/resources/chatbot.png").scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    icon_label.setPixmap(pixmap)

    # Bot name
    text_label = QLabel(bot_name)
    text_label.setFont(QFont("Arial", 16, QFont.Bold))
    text_label.setAlignment(Qt.AlignVCenter)

    # Settings button with menu
    settings_btn = QPushButton("⚙")
    settings_btn.setFixedSize(30, 30)
    settings_btn.setStyleSheet("background-color: white; color: #A52A2A; border-radius: 5px;")

    settings_menu = QMenu()

    # View Terms
    view_terms_action = QAction("View Terms of Use")
    def open_terms():
        try:
            with open("LICENSE", "r") as f1, open("LLAMA 3.2 COMMUNITY LICENSE AGREEMENT", "r") as f2:
                text = f1.read() + "\\n\\n" + f2.read()
        except FileNotFoundError:
            text = "License files not found."
        dialog = TermsDialog(text, text, parent)
        dialog.exec_()
    view_terms_action.triggered.connect(open_terms)
    settings_menu.addAction(view_terms_action)

    # Placeholder for future model selection
    choose_model_action = QAction("Choose Model (coming soon)")
    settings_menu.addAction(choose_model_action)

    settings_btn.setMenu(settings_menu)

    # Layout assembly
    layout.addWidget(icon_label)
    layout.addWidget(text_label)
    layout.addStretch()
    layout.addWidget(settings_btn)

    top_bar.setLayout(layout)
    top_bar.setStyleSheet("background-color: #A52A2A; color: white")

    return top_bar
