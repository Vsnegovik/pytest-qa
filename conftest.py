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