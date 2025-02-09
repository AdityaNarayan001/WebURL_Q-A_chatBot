from utils.url_image import capture_full_page_screenshot
from utils import flush_url_screenshot
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QPushButton, QTextEdit, QLabel, QFrame)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import sys
import ollama


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Website Chat Assistant")
        self.setMinimumSize(1000, 700)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
        """)


        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)


        title_label = QLabel("Website Chat Assistant")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)


        website_frame = QFrame()
        website_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        website_layout = QHBoxLayout(website_frame)
        website_layout.setContentsMargins(15, 15, 15, 15)
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter website URL...")
        self.url_input.setMinimumHeight(40)
        self.url_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #0084ff;
            }
        """)
        website_layout.addWidget(self.url_input)

        load_button = QPushButton("Load Website")
        load_button.setMinimumHeight(40)
        load_button.clicked.connect(self.load_website)
        load_button.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border-radius: 5px;
                padding: 5px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        website_layout.addWidget(load_button)
        
        layout.addWidget(website_frame)


        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                padding: 15px;
                font-size: 14px;
                line-height: 1.6;
            }
        """)
        layout.addWidget(self.chat_display)


        chat_input_frame = QFrame()
        chat_input_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        chat_input_layout = QHBoxLayout(chat_input_frame)
        chat_input_layout.setContentsMargins(15, 15, 15, 15)
        
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Type your message...")
        self.chat_input.setMinimumHeight(45)
        self.chat_input.returnPressed.connect(self.send_message)
        self.chat_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                padding: 5px 15px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #0084ff;
            }
        """)
        chat_input_layout.addWidget(self.chat_input)

        send_button = QPushButton("Send Message")
        send_button.setMinimumHeight(45)
        send_button.clicked.connect(self.send_message)
        send_button.setStyleSheet("""
            QPushButton {
                background-color: #0084ff;
                color: white;
                border-radius: 5px;
                padding: 5px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0073e6;
            }
        """)
        chat_input_layout.addWidget(send_button)
        
        layout.addWidget(chat_input_frame)


        creator_label = QLabel("Made by Aditya Narayan")
        creator_label.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                padding: 10px;
                font-size: 12px;
                font-weight: bold;
            }
        """)
        creator_label.setAlignment(Qt.AlignRight)
        layout.addWidget(creator_label)

    def load_website(self):
        url = self.url_input.text()
        if url:
            flush_url_screenshot()
            try:
                capture_full_page_screenshot(url)
                self.chat_display.append(f"🤖 Website loaded: {url}")
            except Exception as e:
                self.chat_display.append(f"❌ Error loading website: {str(e)}")

    def send_message(self):
        message = self.chat_input.text()
        if message:
            self.chat_display.append(f"\n👤 You: {message}")
            self.chat_display.append("🤖 Assistant: ")
            try:
                response = ollama.chat(
                    model="llava",
                    messages=[{"role": "user", "content": message, "images": ["url_screenshot/screenshot.png"]}]
                )
                self.chat_display.append(response["message"]["content"])
                self.chat_input.clear()
            except Exception as e:
                self.chat_display.append(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())