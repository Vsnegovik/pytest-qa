import pytest
from helpers.api_client import APIClient

@pytest.mark.api
def test_get_user():
    api = APIClient()

    print("Отправляем запрос...")
    response = api.get_user(1)

    print("Ответ получен!", response.status_code)
    assert response.status_code == 200
    assert response.json()["id"] == 1