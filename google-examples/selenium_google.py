from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# 1. ตั้งค่า Options ไม่ให้ปิดเบราว์เซอร์อัตโนมัติ
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# 2. ส่งค่า options เข้าไปที่ webdriver
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.google.com")

search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("Robot Framework" + Keys.RETURN)

# หมายเหตุ: ไม่ต้องใส่ driver.quit() ด้านล่าง
