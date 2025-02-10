import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def browser():
    """Инициализация браузера Playwright перед тестами"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()

@pytest.fixture(scope="session")
def page(browser):
    """Создаем новую страницу браузера перед каждым тестом"""
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture(scope="function")
def authenticated_page():
    username = os.getenv("APP_USERNAME")
    password = os.getenv("APP_PASSWORD")

    assert username and password, "Ошибка: логин и пароль не заданы!"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Авторизация
        page.goto("https://wms.local:8585/sign-in")
        page.fill("[data-test-id='input__phone']", username)
        page.fill("[data-test-id='input__password']", password)
        page.click("[data-test-id='button__signIn']")
        page.wait_for_url("**/dashboard")

        yield page  # Возвращаем авторизованную страницу

        browser.close()