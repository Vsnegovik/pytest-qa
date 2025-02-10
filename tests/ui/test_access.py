import pytest

@pytest.mark.ui
def test_login(page):
    page.goto("https://wms.local:8585/delivery-point")
    page.wait_for_load_state("networkidle")  # Ждём загрузки страницы
    assert "Приёмка" in page.title()