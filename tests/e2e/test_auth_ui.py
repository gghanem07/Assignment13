from playwright.sync_api import sync_playwright
import random
import requests

BASE_URL = "http://localhost:8000"


def unique_user():
    suffix = random.randint(100000, 999999)
    return {
        "username": f"user{suffix}",
        "email": f"user{suffix}@test.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "Password123!",
        "confirm_password": "Password123!",
    }


def register_user_via_api(user_data):
    response = requests.post(f"{BASE_URL}/auth/register", json=user_data, timeout=10)
    assert response.status_code in (200, 201), f"Registration failed: {response.status_code} {response.text}"


def test_register_success():
    user = unique_user()

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

        # success message should appear before redirect
        page.wait_for_timeout(1000)
        assert page.locator("#successAlert").is_visible()

        # page should eventually redirect to login
        page.wait_for_timeout(2500)
        assert "login" in page.url

        browser.close()


def test_login_success():
    user = unique_user()
    register_user_via_api(user)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(f"{BASE_URL}/login")

        page.fill("#username", user["username"])
        page.fill("#password", user["password"])

        page.click("button[type=submit]")

        page.wait_for_timeout(1500)

        # verify login succeeded by checking JWT storage
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
    user = unique_user()
    register_user_via_api(user)

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