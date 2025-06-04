# app/ui/stylesheet.py

def load_stylesheet():
    return """
    QWidget {
        background-color: #FFFFFF;
        font-family: Arial, sans-serif;
        font-size: 14px;
        color: #000000;
    }

    QLabel#TopBar {
        background-color: #A52A2A;
        color: #FFFFFF;
        padding: 10px;
        font-size: 18px;
        font-weight: bold;
    }

    QLineEdit {
        border: 1px solid #CCCCCC;
        padding: 5px;
        border-radius: 4px;
    }

    QPushButton {
        background-color: #800000;
        color: #FFFFFF;
        border: none;
        padding: 5px 10px;
        border-radius: 4px;
    }

    QPushButton:hover {
        background-color: #A52A2A;
    }

    QScrollArea {
        border: none;
    }
    """
