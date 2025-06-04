from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QComboBox, QLabel, QLineEdit, QPushButton, QMessageBox
)
import os

CONFIG_FILE = ".model_config"

class ModelSelectorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Model Settings")
        self.setMinimumWidth(400)

        self.selected_model = "local"
        self.api_key = ""

        self.layout = QVBoxLayout()

        self.model_dropdown = QComboBox()
        self.model_dropdown.addItems(["local", "api"])
        self.model_dropdown.currentTextChanged.connect(self.toggle_api_input)
        self.layout.addWidget(QLabel("Select LLM backend:"))
        self.layout.addWidget(self.model_dropdown)

        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("Enter Hugging Face Inference API Key")
        self.api_key_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.api_key_input)
        self.api_key_input.hide()

        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.save_settings)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)

        self.load_existing_config()

    def toggle_api_input(self, value):
        self.api_key_input.setVisible(value == "api")

    def save_settings(self):
        model_type = self.model_dropdown.currentText()
        new_api_key = self.api_key_input.text().strip()

        # Load existing API key if present
        existing_api_key = self.api_key  # From load_existing_config()

        if model_type == "api" and not new_api_key:
            QMessageBox.warning(self, "Missing API Key", "Please enter a valid API key.")
            return

        # Decide which API key to write
        final_api_key = new_api_key if new_api_key else existing_api_key

        with open(CONFIG_FILE, "w") as f:
            f.write(f"MODEL_TYPE={model_type}\n")
            f.write(f"INFERENCE_API_KEY={final_api_key}\n")

        QMessageBox.information(self, "Saved", "Model settings saved successfully.")
        self.accept()


    def load_existing_config(self):
        if not os.path.exists(CONFIG_FILE):
            return

        with open(CONFIG_FILE, "r") as f:
            for line in f:
                if line.startswith("MODEL_TYPE="):
                    self.selected_model = line.split("=", 1)[1].strip()
                    self.model_dropdown.setCurrentText(self.selected_model)
                elif line.startswith("INFERENCE_API_KEY="):
                    self.api_key = line.split("=", 1)[1].strip()
                    self.api_key_input.setText(self.api_key)

        self.toggle_api_input(self.selected_model)
