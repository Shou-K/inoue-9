import sys
from PySide6.QtWidgets import QApplication
from wordbook_app import WordbookApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WordbookApp()
    window.show()
    sys.exit(app.exec())
