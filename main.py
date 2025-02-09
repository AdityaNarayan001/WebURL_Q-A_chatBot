from utils.url_image import capture_full_page_screenshot
from utils import flush_url_screenshot
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QPushButton, QTextEdit, QLabel)
import sys
import ollama


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Website Chat Assistant")
        self.setMinimumSize(800, 600)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Website section
        website_widget = QWidget()
        website_layout = QHBoxLayout(website_widget)
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter website URL...")
        website_layout.addWidget(self.url_input)

        load_button = QPushButton("Load Website")
        load_button.clicked.connect(self.load_website)
        website_layout.addWidget(load_button)
        
        layout.addWidget(website_widget)

        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background-color: #f0f0f0;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        layout.addWidget(self.chat_display)

        # Chat input section
        chat_input_widget = QWidget()
        chat_input_layout = QHBoxLayout(chat_input_widget)
        
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Type your message...")
        self.chat_input.returnPressed.connect(self.send_message)
        chat_input_layout.addWidget(self.chat_input)

        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_message)
        send_button.setStyleSheet("""
            QPushButton {
                background-color: #0084ff;
                color: white;
                border-radius: 5px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #0073e6;
            }
        """)
        chat_input_layout.addWidget(send_button)
        
        layout.addWidget(chat_input_widget)

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