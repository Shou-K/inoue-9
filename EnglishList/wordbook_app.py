from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QListWidget, QLineEdit, QPushButton, QMessageBox

import sqlite3

class WordbookApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("単語帳 上に単語、下に訳を入力してください")
        self.setGeometry(100, 100, 450, 400)

        # データベースの初期化
        self.init_database()

        # UIの初期化
        self.init_ui()

    def init_database(self):
        self.conn = sqlite3.connect("wordbook.db")
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS words
                            (id INTEGER PRIMARY KEY,
                             word TEXT,
                             translation TEXT)''')
        self.conn.commit()

    def init_ui(self):
        layout = QVBoxLayout()

        self.word_list = QListWidget()
        self.load_words()
        layout.addWidget(self.word_list)

        self.word_input = QLineEdit()
        self.translation_input = QLineEdit()
        layout.addWidget(self.word_input)
        layout.addWidget(self.translation_input)

        self.save_button = QPushButton("保存")
        self.save_button.clicked.connect(self.save_word)
        layout.addWidget(self.save_button)

        self.toggle_translation_button = QPushButton("訳を隠す")
        self.toggle_translation_button.setCheckable(True)
        self.toggle_translation_button.setChecked(False)
        self.toggle_translation_button.clicked.connect(self.toggle_translation)
        layout.addWidget(self.toggle_translation_button)
        
        self.toggle_word_button = QPushButton("単語を隠す")
        self.toggle_word_button.setCheckable(True)
        self.toggle_word_button.setChecked(False)
        self.toggle_word_button.clicked.connect(self.toggle_word)
        layout.addWidget(self.toggle_word_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def load_words(self):
        self.word_list.clear()
        self.cur.execute("SELECT * FROM words")
        words = self.cur.fetchall()
        for word in words:
            self.word_list.addItem(f"{word[1]} - {word[3]}")

    def save_word(self):
        word = self.word_input.text().strip()
        translation = self.translation_input.text().strip()

        if word and translation:
            self.cur.execute("INSERT INTO words (word, translation) VALUES (?, ?)", (word, translation))
            self.conn.commit()
            self.load_words()
            self.word_input.clear()
            self.translation_input.clear()
        else:
            QMessageBox.warning(self, "エラー", "単語、意味、訳を入力してください。")

    def toggle_translation(self):
        if self.toggle_translation_button.isChecked():
            self.toggle_translation_button.setText("訳を表示")
            for i in range(self.word_list.count()):
                item = self.word_list.item(i)
                word,  translation = item.text().split(" - ")
                item.setText(f"{word} - ***")
        else:
            self.toggle_translation_button.setText("訳を隠す")
            self.load_words()
            
    def toggle_word(self):        
        if self.toggle_word_button.isChecked():
            self.toggle_word_button.setText("単語を表示")
            for i in range(self.word_list.count()):
                item = self.word_list.item(i)
                word,  translation = item.text().split(" - ")
                item.setText(f"*** - {translation}")  # 単語を隠すためのダミーテキストを設定
        else:
            self.toggle_word_button.setText("単語を隠す")
            self.load_words()

    def closeEvent(self, event):
        self.conn.close()
        event.accept()
