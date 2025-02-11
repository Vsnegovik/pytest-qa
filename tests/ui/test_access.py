import pytest

@pytest.mark.ui
def test_login(page):
    page.goto("https://wms-frontend-core-release-dev.dev.cluster.kznexpess.com/delivery-point/route-sheets")
    page.wait_for_load_state("networkidle")  # Ждём загрузки страницы
    assert "Приёмка" in page.title()