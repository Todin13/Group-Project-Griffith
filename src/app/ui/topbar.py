from PyQt5.QtWidgets import (
    QWidget, QLabel, QHBoxLayout, QToolButton, QMenu, QAction
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from src.app.ui.terms_dialog import TermsDialog
from src.app.ui.model_selector import ModelSelectorDialog

import os

def read_current_model_type():
    if not os.path.exists(".model_config"):
        return "local"
    with open(".model_config", "r") as f:
        for line in f:
            if line.startswith("MODEL_TYPE="):
                return line.split("=")[1].strip()
    return "local"


def create_top_bar(bot_name="GriffAI", parent=None):
    current_model_type = read_current_model_type()

    top_bar = QWidget(parent)
    layout = QHBoxLayout()
    layout.setContentsMargins(10, 10, 10, 10)
    layout.setSpacing(8)

    icon_label = QLabel()
    pixmap = QPixmap("app/resources/chatbot.png").scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    icon_label.setPixmap(pixmap)

    text_label = QLabel(bot_name)
    text_label.setFont(QFont("Arial", 16, QFont.Bold))
    text_label.setAlignment(Qt.AlignCenter)

    settings_button = QToolButton()
    settings_button.setText("⚙ Settings")
    settings_button.setPopupMode(QToolButton.InstantPopup)
    settings_button.setStyleSheet("background-color: white; color: #A52A2A; padding: 5px; border-radius: 5px;")
    settings_button.setMinimumWidth(120)

    settings_menu = QMenu(parent)
    settings_menu.setMinimumWidth(200)

    view_terms_action = QAction("View Terms of Use", settings_menu)

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
    settings_menu.addAction(view_terms_action)

    # Show current model in label
    model_select_action = QAction(f"Model: {current_model_type}", settings_menu)

    def open_model_settings():
        dialog = ModelSelectorDialog(parent)
        if dialog.exec_():
            updated_model = dialog.selected_model
            model_select_action.setText(f"Model: {updated_model}")

    model_select_action.triggered.connect(open_model_settings)
    settings_menu.addAction(model_select_action)

    settings_button.setMenu(settings_menu)

    layout.addWidget(icon_label)
    layout.addWidget(text_label, stretch=1)
    layout.addWidget(settings_button)

    top_bar.setLayout(layout)
    top_bar.setStyleSheet("background-color: #A52A2A; color: white")

    return top_bar
