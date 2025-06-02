from PyQt5.QtWidgets import (
    QWidget, QLabel, QHBoxLayout, QToolButton, QMenu, QAction
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from app.ui.terms_dialog import TermsDialog

def create_top_bar(bot_name="GriffAI", parent=None):
    top_bar = QWidget(parent)
    layout = QHBoxLayout()
    layout.setContentsMargins(10, 10, 10, 10)
    layout.setSpacing(8)

    # Bot icon
    icon_label = QLabel()
    pixmap = QPixmap("app/resources/chatbot.png").scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    icon_label.setPixmap(pixmap)

    # Bot name
    text_label = QLabel(bot_name)
    text_label.setFont(QFont("Arial", 16, QFont.Bold))
    text_label.setAlignment(Qt.AlignCenter)

    # Settings drop-down with QToolButton
    settings_button = QToolButton()
    settings_button.setText("⚙ Settings")
    settings_button.setPopupMode(QToolButton.InstantPopup)
    settings_button.setStyleSheet("background-color: white; color: #A52A2A; padding: 5px; border-radius: 5px;")
    settings_button.setMinimumWidth(120)

    # Menu — attached to the main app window as parent
    menu = QMenu(parent)
    menu.setMinimumWidth(200)  # Ensure long items are visible

    view_terms_action = QAction("View Terms of Use", menu)

    def open_terms():
        try:
            with open("LICENSE", "r") as f1, open("LLAMA 3.2 COMMUNITY LICENSE AGREEMENT", "r") as f2:
                license1 = f1.read()
                license2 = f2.read()
        except FileNotFoundError:
            license1 = "LICENSE file not found."
            license2 = "LLAMA license file not found."

        dialog = TermsDialog(license1, license2, parent)
        dialog.exec_()

    view_terms_action.triggered.connect(open_terms)
    menu.addAction(view_terms_action)
    menu.addAction("Choose Model (coming soon)")

    settings_button.setMenu(menu)

    # Layout assembly
    layout.addWidget(icon_label)
    layout.addWidget(text_label, stretch=1)
    layout.addWidget(settings_button)

    top_bar.setLayout(layout)
    top_bar.setStyleSheet("background-color: #A52A2A; color: white")

    return top_bar
