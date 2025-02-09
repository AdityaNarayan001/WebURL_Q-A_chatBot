from playwright.sync_api import sync_playwright

def capture_full_page_screenshot(url, output_path="url_screenshot/screenshot.png"):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, wait_until="load")

        for _ in range(10): 
            page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
            page.wait_for_timeout(1000) 

        page.screenshot(path=output_path, full_page=True)
        browser.close()
        print(f"🟢 Screenshot saved to {output_path}")
