import pytest
from selenium.webdriver.common.by import By
from conftest import BASE_URL


def login(driver, username, password):
    """keyword ที่ใช้ซ้ำ: เปิดหน้า login แล้วกรอก username / password"""
    driver.get(BASE_URL + "/")
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()


def test_login_success(driver):
    login(driver, "standard_user", "secret_sauce")
    assert driver.find_element(By.CSS_SELECTOR, ".title").text == "Products"


@pytest.mark.parametrize("username, password, expected_error", [
    ("standard_user", "wrong_pass", "Username and password do not match"),
    ("", "secret_sauce", "Username is required"),
    ("standard_user", "", "Password is required"),
    ("locked_out_user", "secret_sauce", "locked out"),
])
def test_login_fail(driver, username, password, expected_error):
    login(driver, username, password)
    error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text
    assert expected_error in error


def test_add_to_cart(driver):
    login(driver, "standard_user", "secret_sauce")
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    assert driver.find_element(By.CSS_SELECTOR, ".shopping_cart_badge").text == "1"
