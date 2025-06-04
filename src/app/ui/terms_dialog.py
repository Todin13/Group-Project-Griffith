from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QPushButton, QTextEdit,
    QCheckBox, QStackedWidget, QMessageBox
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

    def create_license_page(self, license_text, accept_text):
        layout = QVBoxLayout()

        license_box = QTextEdit()
        license_box.setReadOnly(True)
        license_box.setPlainText(license_text)

        accept_checkbox = QCheckBox(accept_text)
        accept_checkbox.setVisible(False)

        decline_checkbox = QCheckBox("I do not accept")
        decline_checkbox.setVisible(False)

        button = QPushButton("Continue" if "general" in accept_text else "Finish")
        button.setEnabled(False)

        # Logic: show checkboxes only at scroll bottom
        def check_scroll():
            scroll = license_box.verticalScrollBar()
            if scroll.value() == scroll.maximum():
                accept_checkbox.setVisible(True)
                decline_checkbox.setVisible(True)

        license_box.verticalScrollBar().valueChanged.connect(check_scroll)

        # Disable accept if decline is checked and vice versa
        def sync_checkboxes():
            if accept_checkbox.isChecked():
                decline_checkbox.setChecked(False)
            if decline_checkbox.isChecked():
                accept_checkbox.setChecked(False)

            # Enable button only if one of them is checked
            button.setEnabled(accept_checkbox.isChecked() or decline_checkbox.isChecked())

        accept_checkbox.stateChanged.connect(sync_checkboxes)
        decline_checkbox.stateChanged.connect(sync_checkboxes)

        layout.addWidget(license_box)
        layout.addWidget(accept_checkbox)
        layout.addWidget(decline_checkbox)
        layout.addWidget(button)

        container = QDialog()
        container.setLayout(layout)

        if "general" in accept_text:
            def next_step():
                if decline_checkbox.isChecked():
                    if self.confirm_exit():
                        self.reject()
                else:
                    self.show_page2()
            button.clicked.connect(next_step)
        else:
            def final_step():
                if decline_checkbox.isChecked():
                    if self.confirm_exit():
                        self.reject()
                else:
                    self.accept()
            button.clicked.connect(final_step)

        return container

    def confirm_exit(self):
        reply = QMessageBox.question(
            self,
            "Are you sure?",
            "You have selected 'I do not accept'. This will close the application.\nDo you really want to exit?",
            QMessageBox.Yes | QMessageBox.No
        )
        return reply == QMessageBox.Yes

    def show_page1(self):
        self.stack.setCurrentWidget(self.page1)

    def show_page2(self):
        self.stack.setCurrentWidget(self.page2)