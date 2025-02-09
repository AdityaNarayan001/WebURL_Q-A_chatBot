import os
import shutil

def flush_url_screenshot():
    if os.path.exists("url_screenshot"):
        shutil.rmtree("url_screenshot")
    os.makedirs("url_screenshot")