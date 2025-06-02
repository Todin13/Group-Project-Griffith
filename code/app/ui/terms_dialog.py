from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QPushButton, QTextEdit,
    QCheckBox, QStackedWidget, QScrollBar
)
from PyQt5.QtCore import Qt


class TermsDialog(QDialog):
    def __init__(self, license1_text, license2_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Conditions of Use")
        self.setMinimumSize(700, 550)

        self.license1_text = license1_text
        self.license2_text = license2_text

        self.stack = QStackedWidget()
        self.page1 = self.create_license_page(
            self.license1_text,
            "I accept the general terms of use"
        )
        self.page2 = self.create_license_page(
            self.license2_text,
            "I accept the LLaMA 3.2 Community License"
        )

        self.stack.addWidget(self.page1)
        self.stack.addWidget(self.page2)

        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        self.setLayout(layout)

        self.show_page1()

    def create_license_page(self, license_text, checkbox_text):
        layout = QVBoxLayout()

        license_box = QTextEdit()
        license_box.setReadOnly(True)
        license_box.setPlainText(license_text)

        checkbox = QCheckBox(checkbox_text)
        checkbox.setVisible(False)  # Hidden until scroll reaches bottom

        button = QPushButton("Continue" if "general" in checkbox_text else "Finish")
        button.setEnabled(False)

        checkbox.stateChanged.connect(lambda state: button.setEnabled(state == Qt.Checked))

        def check_scroll():
            scroll = license_box.verticalScrollBar()
            if scroll.value() == scroll.maximum():
                checkbox.setVisible(True)

        license_box.verticalScrollBar().valueChanged.connect(lambda: check_scroll())

        layout.addWidget(license_box)
        layout.addWidget(checkbox)
        layout.addWidget(button)

        container = QDialog()
        container.setLayout(layout)

        if "general" in checkbox_text:
            button.clicked.connect(self.show_page2)
        else:
            button.clicked.connect(self.accept)

        return container

    def show_page1(self):
        self.stack.setCurrentWidget(self.page1)

    def show_page2(self):
        self.stack.setCurrentWidget(self.page2)