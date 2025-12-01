from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextBrowser, QPushButton
import sqlite3

class ChatHistoryWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat History")
        self.setGeometry(100, 100, 600, 400)
        self.layout = QVBoxLayout()
        self.text_browser = QTextBrowser()
        self.layout.addWidget(self.text_browser)
        self.setLayout(self.layout)
        self.load_chat_history()

    def load_chat_history(self):
        try:
            conn = sqlite3.connect('chat_history.db')
            cursor = conn.cursor()
            cursor.execute('SELECT user_input, jarvis_response, timestamp FROM chat_history ORDER BY timestamp DESC')
            rows = cursor.fetchall()
            conn.close()

            self.text_browser.clear()
            if rows:
                for row in rows:
                    user_input, jarvis_response, timestamp = row
                    self.text_browser.append(f"{timestamp} - You: {user_input}")
                    self.text_browser.append(f"{timestamp} - Jarvis: {jarvis_response}")
                    self.text_browser.append("")
            else:
                self.text_browser.append("No chat history found.")
        except sqlite3.Error as e:
            self.text_browser.append(f"Error loading chat history: {e}")
