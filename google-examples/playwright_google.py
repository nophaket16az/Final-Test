from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # เปิด Chrome (headless=False เพื่อให้เห็นหน้าจอ)
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://www.google.com")

    # พิมพ์คำค้นหาและกด Enter
    page.fill('textarea[name="q"]', 'Cypress')
    page.keyboard.press('Enter')

    # รอผลลัพธ์
    page.wait_for_timeout(3000)
    browser.close()
