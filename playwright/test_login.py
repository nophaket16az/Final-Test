import pytest
from playwright.sync_api import Page, expect
from conftest import BASE_URL

# fixture `page` มาจาก pytest-playwright: เปิด/ปิดเบราว์เซอร์ให้อัตโนมัติ


def login(page: Page, username, password):
    page.goto(BASE_URL + "/")
    page.fill("#user-name", username)
    page.fill("#password", password)
    page.click("#login-button")


def test_login_success(page: Page):
    login(page, "standard_user", "secret_sauce")
    expect(page.locator(".title")).to_have_text("Products")


@pytest.mark.parametrize("username, password, expected_error", [
    ("standard_user", "wrong_pass", "Username and password do not match"),
    ("", "secret_sauce", "Username is required"),
    ("standard_user", "", "Password is required"),
    ("locked_out_user", "secret_sauce", "locked out"),
])
def test_login_fail(page: Page, username, password, expected_error):
    login(page, username, password)
    expect(page.locator("[data-test='error']")).to_contain_text(expected_error)


def test_add_to_cart(page: Page):
    login(page, "standard_user", "secret_sauce")
    page.click("#add-to-cart-sauce-labs-backpack")
    expect(page.locator(".shopping_cart_badge")).to_have_text("1")
