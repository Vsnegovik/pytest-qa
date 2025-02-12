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

    with sync_playwright() as p:
        """Логинимся в Keycloak через браузер перед каждым тестом"""
        username = os.getenv("KEYCLOAK_USERNAME")
        password = os.getenv("KEYCLOAK_PASSWORD")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Переход на страницу логина Keycloak
        page.goto("https://auth.infra.cluster.kznexpess.com/realms/kazanexpress/protocol/openid-connect/auth?approval_prompt=force&client_id=developer-oauth-client&redirect_uri=https%3A%2F%2Foauth2.dev.cluster.kznexpess.com%2Foauth2%2Fcallback&response_type=code&scope=openid+profile+email&state=hkWV5Lk6yD88rcXaZtDSb7Kp2JGWKyM6HfgRWaoGdLY%3Ahttps%3A%2F%2Fwms-frontend-core-release-dev.dev.cluster.kznexpess.com%2Fassembly%2FACTIVE")
        page.click("#social-magnit-oidc")
        page.wait_for_load_state("networkidle")
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