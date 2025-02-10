import pytest
from dotenv import load_dotenv
import os

load_dotenv()
username = os.getenv("APP_USERNAME")
password = os.getenv("APP_PASSWORD")

@pytest.mark.ui
def test_login(page):
    page.goto("https://wms.local:8585/sign-in")
    page.fill("[data-test-id='input__phone']", username)
    page.fill("[data-test-id='input__password']", password)
    page.click("[data-test-id='button__signIn']")
    page.wait_for_load_state("networkidle")  # Ждём загрузки страницы
    assert "Домашняя" in page.title()