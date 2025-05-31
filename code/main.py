from PyQt5.QtWidgets import QApplication
import sys
from app.ui.stylesheet import load_stylesheet
from app.window import ChatApp  # You’ll need to implement this

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet())
    window = ChatApp()
    window.show()
    sys.exit(app.exec_())
