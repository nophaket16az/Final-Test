import pytest
from playwright.sync_api import Page, expect
from conftest import BASE_URL

# EP + BVA ของกฎ "อายุ 18-60"
@pytest.mark.parametrize("age, expected", [
    ("10", "Age must be between 18 and 60"),   # EP invalid
    ("35", "Valid age"),                       # EP valid
    ("70", "Age must be between 18 and 60"),   # EP invalid
    ("17", "Age must be between 18 and 60"),   # BVA min-1
    ("18", "Valid age"),                       # BVA min
    ("19", "Valid age"),                       # BVA min+1
    ("59", "Valid age"),                       # BVA max-1
    ("60", "Valid age"),                       # BVA max
    ("61", "Age must be between 18 and 60"),   # BVA max+1
    ("", "Age is required"),
    ("abc", "Age must be a number"),
])
def test_age(page: Page, age, expected):
    page.goto(BASE_URL + "/register.html")
    page.fill("#age", age)
    page.click("#submit")
    expect(page.locator("#result")).to_have_text(expected)
