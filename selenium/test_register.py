import pytest
from selenium.webdriver.common.by import By
from conftest import BASE_URL

# EP (Equivalence Partitioning) + BVA (Boundary Value Analysis) ของกฎ "อายุ 18-60"
@pytest.mark.parametrize("age, expected", [
    ("10", "Age must be between 18 and 60"),   # EP: invalid ต่ำกว่า
    ("35", "Valid age"),                       # EP: valid
    ("70", "Age must be between 18 and 60"),   # EP: invalid สูงกว่า
    ("17", "Age must be between 18 and 60"),   # BVA: min-1
    ("18", "Valid age"),                       # BVA: min
    ("19", "Valid age"),                       # BVA: min+1
    ("59", "Valid age"),                       # BVA: max-1
    ("60", "Valid age"),                       # BVA: max
    ("61", "Age must be between 18 and 60"),   # BVA: max+1
    ("", "Age is required"),                   # ช่องว่าง (error guessing)
    ("abc", "Age must be a number"),           # ตัวอักษรในช่องตัวเลข (error guessing)
])
def test_age(driver, age, expected):
    driver.get(BASE_URL + "/register.html")
    driver.find_element(By.ID, "age").send_keys(age)
    driver.find_element(By.ID, "submit").click()
    assert driver.find_element(By.ID, "result").text == expected
