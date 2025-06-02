import os
import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QRect
from app.ui.chatbar import create_chat_bar
from app.ui.topbar import create_top_bar
from app.ui.bubble import create_chat_bubble
from core.use_model import ask_model
from app.ui.terms_dialog import TermsDialog

class ChatApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Griffith College History Assistant")
        self.setMinimumSize(500, 600)

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
            from app.ui.terms_dialog import TermsDialog

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

        self.scroll_content = QWidget()
        self.scroll_content.setLayout(self.chat_area)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll)

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

        user_bubble, _ = create_chat_bubble(user_input, is_user=True)
        self.chat_area.addWidget(user_bubble)

        self.input_field.clear()

        self.typing_label, _ = create_chat_bubble("GriffAI is typing...", is_user=False, bot_name="GriffithAI")
        self.chat_area.addWidget(self.typing_label)

        self.scroll.verticalScrollBar().setValue(self.scroll.verticalScrollBar().maximum())

        # Fetch model response and display it
        QTimer.singleShot(100, lambda: self.fetch_and_display_response(user_input))


    def fetch_and_display_response(self, user_input):
        response = ask_model(user_input).strip()
        self.typing_label.deleteLater()

        self.bot_response = response
        self.char_index = 0
        
        self.animated_bubble, self.label = create_chat_bubble("", is_user=False, bot_name="GriffithAI")
        self.chat_area.addWidget(self.animated_bubble)

        self.scroll.verticalScrollBar().setValue(self.scroll.verticalScrollBar().maximum())

        self.typing_timer = QTimer()
        self.typing_timer.timeout.connect(self.animate_typing)
        self.typing_timer.start(15)


    def animate_typing(self):
        if self.char_index < len(self.bot_response):
            self.label.setText(self.bot_response[:self.char_index + 1])
            self.char_index += 1
            self.scroll.verticalScrollBar().setValue(self.scroll.verticalScrollBar().maximum())
        else:
            self.typing_timer.stop()

