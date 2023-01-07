from functools import cached_property
from pydantic import BaseModel
from pathlib import Path
from orjson import loads
from httpx import post


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

    def __repr__(self):
        return f"{self.role} @{self.username}: {self.disk_usage}/{self.disk_limit} {self.email}"


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


class BaseUser:
    def __init__(self, token: str = None, username: str = None, email: str = None, password: str = None):
        self._token = token
        self._username = username
        self._email = email
        self._password = password

    @cached_property
    def token(self):
        return self._token or self.fetch_token()

    def fetch_token(self) -> str:
        res = loads(post(
            "https://smms.app/api/v2/token",
            data={"username": self._username or self._email, "password": self._password}
        ).content)
        try:
            return res["data"]["token"]
        except KeyError as err:
            raise ValueError(res) from err

    @cached_property
    def http_client(self):
        return self.get_http_client()

    def get_http_client(self):
        raise NotImplementedError

    def upload(self, filename: str, file, media_type: str):
        raise NotImplementedError

    def upload_file(self, path):
        filename = Path(path).name
        return self.upload(Path(path).name, open(path, "rb"), filename.split(".")[-1])
