from requests import get, post
from orjson import loads


def clear_temp_upload_history(token):
    return loads(get(
        "https://sm.ms/api/v2/clear",
        headers={"Authorization": token}
    ).content)


def get_temp_upload_history(token):
    return loads(get(
        "https://sm.ms/api/v2/history",
        headers={"Authorization": token}
    ).content)


def get_upload_history(token, page):
    return loads(get(
        f"https://sm.ms/api/v2/history?{page=}",
        headers={"Authorization": token}
    ).content)


# noinspection PyShadowingBuiltins
def delete_image(token, hash):
    return loads(get(
        f"https://sm.ms/api/v2/delete/{hash}",
        headers={"Authorization": token}
    ).content)


def upload_image(token, filename, file=None):
    return loads(post(
        "https://sm.ms/api/v2/upload",
        files={"smfile": (filename, file or open(filename, "rb"))},
        headers={"Authorization": token}
    ).content)
