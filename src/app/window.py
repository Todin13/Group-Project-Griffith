import os
import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QRect
from src.app.ui.chatbar import create_chat_bar
from src.app.ui.topbar import create_top_bar
from src.app.ui.bubble import Bubble
from src.app.ui.terms_dialog import TermsDialog
from src.core.local_llm import local_llm_question
from src.core.api_llm import api_llm_question
from src.core.pinecone_retrival import get_context_retrieval  # or faiss_retrieval


def choose_model(user_input):
    model_type = "local"
    api_key = None
    if os.path.exists(".model_config"):
        with open(".model_config", "r") as f:
            for line in f:
                if line.startswith("MODEL_TYPE="):
                    model_type = line.split("=")[1].strip()
                elif line.startswith("INFERENCE_API_KEY="):
                    api_key = line.split("=")[1].strip()

    if model_type == "api":
        return api_llm_question(user_input, get_context_retrieval, api_key)
    else:
        return local_llm_question(user_input, get_context_retrieval)


class ChatApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Griffith College History Assistant")
        self.setMinimumSize(500, 600)

        self.llm_backend = "local"
        self.init_ui()
        self.check_license_agreement()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.layout.addWidget(create_top_bar("GrifftihAI"), stretch=0)

        # Create chatbar widget once here
        self.chatbar_widget, self.input_field = create_chat_bar(self.send_message)

        # Placeholder widget to center chatbar and label vertically
        self.placeholder_widget = QWidget()
        placeholder_layout = QVBoxLayout()
        placeholder_layout.setAlignment(Qt.AlignCenter)

        # Then add margins (left, top, right, bottom)
        self.placeholder_widget.setContentsMargins(50, 0, 50, 0)  # 50px left & right margin
        

        self.help_label = QLabel("How can I help you?")
        self.help_label.setAlignment(Qt.AlignCenter)
        placeholder_layout.addWidget(self.help_label)

        placeholder_layout.addWidget(self.chatbar_widget)
        self.placeholder_widget.setLayout(placeholder_layout)



        self.layout.addWidget(self.placeholder_widget, stretch=3)

        # Variables for chat area and scroll
        self.chat_area = None
        self.scroll = None
        self.typing_label = None


    def check_license_agreement(self):
        if not os.path.exists(".accepted_terms"):

            try:
                with open("LICENSE", "r") as f1, open("LLAMA 3.2 COMMUNITY LICENSE AGREEMENT", "r") as f2:
                    license1 = f1.read()
                    license2 = f2.read()
            except FileNotFoundError:
                license1 = "LICENSE file not found."
                license2 = "LLAMA license file not found."

            dialog = TermsDialog(license1, license2, self)
            if dialog.exec_():
                with open(".accepted_terms", "w") as f:
                    f.write("accepted")
            else:
                print("User declined terms.")
                sys.exit(0)




    def setup_chat_ui(self):
        # Remove the placeholder widget (with label + chatbar)
        self.layout.removeWidget(self.placeholder_widget)
        self.placeholder_widget.hide()

        # Create scrollable chat area
        self.chat_area = QVBoxLayout()
        self.chat_area.setAlignment(Qt.AlignTop)

        self.scroll_widget = QWidget()
        self.scroll_widget.setLayout(self.chat_area)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.layout.insertWidget(1, self.scroll, stretch=1)

        self.scroll.setWidget(self.scroll_widget)
        self.scroll.setStyleSheet("border: none;")

        # Animate chatbar moving from center to bottom

        # Remove chatbar from placeholder_layout
        self.chatbar_widget.setParent(None)  # remove from old layout

        # Optional: Animate the chatbar sliding up from center to bottom
        self.animate_chatbar_transition()

        # Add chatbar at the bottom of main layout (below scroll)
        
        self.layout.addWidget(self.chatbar_widget)


    def animate_chatbar_transition(self):
        # We'll animate the geometry of the chatbar_widget

        # Get starting geometry relative to main window
        start_rect = self.chatbar_widget.geometry()
        # We'll animate the chatbar from roughly center Y to bottom Y

        # Calculate end rect: same width/height but positioned at bottom
        parent_geom = self.geometry()
        chatbar_height = self.chatbar_widget.sizeHint().height()
        end_y = parent_geom.height() - chatbar_height - 10  # 10 px margin from bottom
        end_rect = QRect(start_rect.x(), end_y, start_rect.width(), chatbar_height)

        self.anim = QPropertyAnimation(self.chatbar_widget, b"geometry")
        self.anim.setDuration(500)  # half second
        self.anim.setStartValue(start_rect)
        self.anim.setEndValue(end_rect)
        self.anim.start()

    def send_message(self):
        user_input = self.input_field.text().strip()
        if not user_input:
            return

        if self.chat_area is None:
            self.setup_chat_ui()
        
        if user_input:
            self.add_message(user_input, is_user=True)
            self.input_field.clear()

        self.typing_label = QLabel("GriffithAI is typing...")
        self.typing_label.setStyleSheet("color: gray; font-style: italic; margin: 10px;")
        self.chat_area.addWidget(self.typing_label)


        self.scroll.verticalScrollBar().setValue(self.scroll.verticalScrollBar().maximum())

        # Fetch model response and display it
        QTimer.singleShot(100, lambda: self.fetch_and_display_response(user_input))


    def add_message(self, message, is_user):
        bubble = Bubble(message, is_user)
        container = QHBoxLayout()
        if is_user:
            container.addStretch()
            container.addWidget(bubble)
        else:
            container.addWidget(bubble)
            container.addStretch()

        wrapper = QWidget()
        wrapper.setLayout(container)
        self.chat_area.addWidget(wrapper)
        self.scroll.verticalScrollBar().setValue(self.scroll.verticalScrollBar().maximum())

    from PyQt5.QtCore import QTimer

    def fetch_and_display_response(self, user_input):
        # Get the model's response
        response = choose_model(user_input).strip()

        # Remove typing indicator if it exists
        if hasattr(self, 'typing_label') and self.typing_label:
            self.typing_label.deleteLater()
            self.typing_label = None

        # Prepare for animation
        self.bot_response = response
        self.char_index = 0

        # Add the bot message bubble with empty text first
        self.animated_bubble = Bubble("", is_user=False)
        container = QHBoxLayout()
        container.addWidget(self.animated_bubble)
        container.addStretch()

        wrapper = QWidget()
        wrapper.setLayout(container)

        self.chat_area.addWidget(wrapper)
        self.scroll.verticalScrollBar().setValue(self.scroll.verticalScrollBar().maximum())

        # Animate the typing effect
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_bot_typing)
        self.timer.start(30)  # adjust typing speed

    def animate_bot_typing(self):
        if self.char_index < len(self.bot_response):
            # Append the next character to the bubble text
            current_text = self.animated_bubble.text()
            self.animated_bubble.setText(current_text + self.bot_response[self.char_index])

            self.char_index += 1
        else:
            # Stop the timer when done
            self.timer.stop()
            self.timer.deleteLater()
            self.timer = None

        # Scroll to the bottom
        self.scroll.verticalScrollBar().setValue(self.scroll.verticalScrollBar().maximum())