from playwright.sync_api import sync_playwright

BASE_URL = "http://localhost:8000"


def test_register_success():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(f"{BASE_URL}/register")

        # use unique user to avoid duplicates
        import random
        username = f"user{random.randint(1000,9999)}"
        email = f"{username}@test.com"

        page.fill("#username", username)
        page.fill("#email", email)
        page.fill("#first_name", "Test")
        page.fill("#last_name", "User")
        page.fill("#password", "Password123!")
        page.fill("#confirm_password", "Password123!")

        page.click("button[type=submit]")

        # wait for redirect to login
        page.wait_for_url("**/login")

        assert "login" in page.url

        browser.close()


def test_login_success():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(f"{BASE_URL}/login")

        page.fill("#username", "testuser123")
        page.fill("#password", "Password123!")

        page.click("button[type=submit]")

        # wait for redirect to dashboard
        page.wait_for_url("**/dashboard")

        # verify JWT stored
        token = page.evaluate("localStorage.getItem('access_token')")
        assert token is not None

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
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(f"{BASE_URL}/login")

        page.fill("#username", "testuser123")
        page.fill("#password", "wrongpassword")

        page.click("button[type=submit]")

        page.wait_for_timeout(1000)

        assert page.locator("#errorAlert").is_visible()

        browser.close()