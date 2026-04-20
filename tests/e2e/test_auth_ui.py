from playwright.sync_api import sync_playwright
import random
import requests

BASE_URL = "http://localhost:8000"


def create_user():
    suffix = random.randint(100000, 999999)
    return {
        "username": f"user{suffix}",
        "email": f"user{suffix}@test.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "Password123!",
        "confirm_password": "Password123!",
    }


def register_api(user):
    r = requests.post(f"{BASE_URL}/auth/register", json=user)
    assert r.status_code in (200, 201), r.text


def test_register_success():
    user = create_user()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(f"{BASE_URL}/register")

        page.fill("#username", user["username"])
        page.fill("#email", user["email"])
        page.fill("#first_name", user["first_name"])
        page.fill("#last_name", user["last_name"])
        page.fill("#password", user["password"])
        page.fill("#confirm_password", user["confirm_password"])

        page.click("button[type=submit]")

        # check success message (NOT redirect)
        page.wait_for_timeout(1000)
        assert page.locator("#successAlert").is_visible()

        browser.close()


def test_login_success():
    user = create_user()
    register_api(user)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(f"{BASE_URL}/login")

        page.fill("#username", user["username"])
        page.fill("#password", user["password"])

        page.click("button[type=submit]")

        page.wait_for_timeout(1500)

        token = page.evaluate("localStorage.getItem('access_token')")
        assert token is not None and token != ""

        browser.close()


def test_register_short_password():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(f"{BASE_URL}/register")

        page.fill("#username", "shortpassuser")
        page.fill("#email", "shortpassuser@example.com")
        page.fill("#first_name", "Short")
        page.fill("#last_name", "Pass")
        page.fill("#password", "short")
        page.fill("#confirm_password", "short")

        page.click("button[type=submit]")

        page.wait_for_timeout(1000)
        assert page.locator("#errorAlert").is_visible()

        browser.close()


def test_login_invalid_password():
    user = create_user()
    register_api(user)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(f"{BASE_URL}/login")

        page.fill("#username", user["username"])
        page.fill("#password", "wrongpassword")

        page.click("button[type=submit]")

        page.wait_for_timeout(1000)
        assert page.locator("#errorAlert").is_visible()

        browser.close()