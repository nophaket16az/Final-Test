import os

# เปลี่ยนเว็บที่จะทดสอบได้ด้วยตัวแปร BASE_URL เช่น  BASE_URL=https://www.saucedemo.com
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000").rstrip("/")
