from utils.llm import chat
from utils.url_image import capture_full_page_screenshot
from utils import flush_url_screenshot

URL = "https://ai4bharat.iitm.ac.in/"
CHAT = "Tell me about the website layout."

flush_url_screenshot()

capture_full_page_screenshot(URL)
chat(CHAT, "url_screenshot/screenshot.png")