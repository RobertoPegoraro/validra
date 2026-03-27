import requests

BASE_URL = "http://localhost:8000"


def run_test(config):

    response = requests.post(
        f"{BASE_URL}/run",
        json=config
    )

    response.raise_for_status()

    return response.json()