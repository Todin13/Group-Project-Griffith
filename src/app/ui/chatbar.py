from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

def create_chat_bar(on_submit_callback):
    container = QWidget()  # Wrapper widget that we will style
    container.setObjectName("chatbarContainer")
    
    input_field = QLineEdit()
    input_field.setPlaceholderText("Ask a question...")
    
    send_btn = QPushButton()
    send_btn.setIcon(QIcon("app/resources/send.png"))
    send_btn.setIconSize(QSize(24, 24))
    send_btn.setStyleSheet("border: none;")
    
    input_field.returnPressed.connect(on_submit_callback)
    send_btn.clicked.connect(on_submit_callback)
    
    layout = QHBoxLayout()
    layout.addWidget(input_field)
    layout.addWidget(send_btn)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(5)
    
    container.setLayout(layout)

    # Add stylesheet for grey background and rounded corners
    container.setStyleSheet("""
        QWidget#chatbarContainer {
            background-color: #f0f0f0;       /* light grey */
            border-radius: 12px;
            border: 1px solid #ccc;
        }
        QLineEdit {
            border: none;
            background: transparent;
            font-size: 14px;
            padding: 5px;
        }
        QPushButton {
            background: transparent;
        }
    """)

    return container, input_field