import os
import pytest
import requests

from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser():
    """Инициализация браузера Playwright перед тестами"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
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
    """Логинимся в Keycloak через браузер перед каждым тестом"""
    username = os.getenv("KEYCLOAK_USERNAME")
    password = os.getenv("KEYCLOAK_PASSWORD")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Переход на страницу логина Keycloak
        page.goto("https://keycloak.example.com/auth/realms/myrealm/protocol/openid-connect/auth?client_id=myclient&response_type=code")

        # Ввод логина и пароля
        page.fill("#username", username)
        page.fill("#password", password)
        page.click("#kc-login")

        page.wait_for_load_state("networkidle")

        yield page  # Возвращаем авторизованную страницу

        username = os.getenv("APP_USERNAME")
        password = os.getenv("APP_PASSWORD")

        assert username and password, "Ошибка: логин и пароль не заданы!"
        
        # Авторизация
        page.goto("https://wms-frontend-core-release-dev.dev.cluster.kznexpess.com/sign-in")
        page.fill("[data-test-id='input__phone']", username)
        page.fill("[data-test-id='input__password']", password)
        page.click("[data-test-id='button__signIn']")
        page.wait_for_url("**/dashboard")

        yield page  # Возвращаем авторизованную страницу

        browser.close()