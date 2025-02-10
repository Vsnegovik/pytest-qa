import pytest
import requests

@pytest.mark.api
class APIClient:
    BASE_URL = "https://jsonplaceholder.typicode.com"

    def get_user(self, user_id):
        response = requests.get(f"{self.BASE_URL}/users/{user_id}", timeout=5)
        return response