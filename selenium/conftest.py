import os
import pytest
from selenium import webdriver

# เปลี่ยนเว็บที่จะทดสอบได้ด้วยตัวแปร BASE_URL เช่น  BASE_URL=https://www.saucedemo.com
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000").rstrip("/")


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    if os.getenv("HEADLESS") == "1":          # HEADLESS=1 = รันแบบไม่เปิดหน้าต่าง
        options.add_argument("--headless=new")
    if os.getenv("NO_SANDBOX") == "1":        # ใช้ตอนรันบน Linux/Docker/Jenkins ด้วย root
        options.add_argument("--no-sandbox")
    d = webdriver.Chrome(options=options)      # Selenium Manager หา ChromeDriver ให้เอง
    d.implicitly_wait(5)                       # รอ element สูงสุด 5 วินาที
    yield d
    d.quit()                                   # ปิดเบราว์เซอร์หลังจบแต่ละ test
