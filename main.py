from requests import get, post
from orjson import dumps, loads
from functools import cache


def request_token(username, password) -> dict:
    return loads(post(
        "https://sm.ms/api/v2/token", {"username": username, "password": password}
    ).content)


@cache
def get_token(username, password):
    response = request_token(username, password)
    assert response["success"]
    assert response["code"] == "success"
    assert response["message"] == "Get API token success."
    return response["data"]["token"]
