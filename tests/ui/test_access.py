import pytest

@pytest.mark.ui
def test_login(authenticated_page):
    authenticated_page.goto("https://wms-frontend-core-release-dev.dev.cluster.kznexpess.com/delivery-point/route-sheets")
    authenticated_page.wait_for_load_state("networkidle")  # Ждём загрузки страницы
    assert "Приёмка" in authenticated_page.title()