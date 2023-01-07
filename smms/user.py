from orjson import loads
from httpx import Client
from functools import cached_property
from pydantic import BaseModel
from pathlib import Path


class UserProfile(BaseModel):
    username: str
    email: str
    role: str
    group_expire: str
    email_verified: bool
    disk_usage: str
    disk_usage_raw: int
    disk_limit: str
    disk_limit_raw: int

    __name__ = "User"


class ImageUploaded(BaseModel):
    width: int
    height: int
    filename: str
    storename: str
    size: int
    path: str
    hash: str
    url: str
    delete: str
    page: str

    def __repr__(self):
        return f"Image< {self.width}x{self.height} {self.hash} - {self.filename} >"


class UploadHistoryItem(ImageUploaded):
    created_at: str

    def __repr__(self):
        return f"Image< {self.width}x{self.height} {self.created_at} {self.hash} - {self.filename} >"


class User:
    def __init__(self, token: str = None, username: str = None, email: str = None, password: str = None):
        self._token = token
        self._username = username
        self._email = email
        self._password = password

    @cached_property
    def http_client(self):
        return self.get_http_client()

    def get_http_client(self):
        return Client(
            http2=True,
            base_url="https://smms.app/api/v2/",
            headers={"Authorization": f"Basic {self.token}"}
        )

    @cached_property
    def token(self):
        return self._token or self.fetch_token()

    def fetch_token(self) -> str:
        res = loads(self.http_client.post(
            "/token", data={"username": self._username or self._email, "password": self._password}
        ).content)
        try:
            return res["data"]["token"]
        except KeyError as err:
            raise ValueError(res) from err

    @property
    def user_profile(self) -> UserProfile:
        res = loads(self.http_client.post("/profile").content)
        try:
            return UserProfile(**res["data"])
        except KeyError as err:
            raise ValueError(res) from err

    def fetch_upload_history(self, page: int) -> list[UploadHistoryItem]:
        res = loads(self.http_client.get(f"/upload_history?{page=}").content)
        try:
            return [UploadHistoryItem(**item) for item in res["data"]]
        except KeyError as err:
            raise ValueError(res) from err

    @property
    def history(self) -> list[UploadHistoryItem]:
        results = result = self.fetch_upload_history(0)
        page = 0
        while len(result) == 100:
            page += 1
            result = self.fetch_upload_history(page)
            results.extend(result)

        return results

    def upload(self, filename: str, file, media_type: str) -> ImageUploaded:
        response = self.http_client.post("/upload", files={"smfile": (filename, file, media_type)})
        print(response.headers)

        res = loads(response.content)
        try:
            return ImageUploaded(**res["data"])
        except KeyError as err:
            raise ValueError(res) from err

    def upload_file(self, path: str) -> ImageUploaded:
        filename = Path(path).name
        return self.upload(Path(path).name, open(path, "rb"), filename.split(".")[-1])

    def delete(self, hash: str):
        return loads(self.http_client.get(f"/delete/{hash}").content)
