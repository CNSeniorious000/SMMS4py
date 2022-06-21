from requests import post
from orjson import loads
from functools import cached_property
from cachetools.func import ttl_cache

TTL = 5


# noinspection PyPropertyAccess, PyAttributeOutsideInit
class BaseUser:
    @classmethod
    def request_token(cls, username, password) -> str:
        response = loads(post(
            "https://sm.ms/api/v2/token",
            {"username": username, "password": password}
        ).content)
        assert all((
            response["success"],
            response["code"] == "success",
            response["message"] == "Get API token success."
        )), "not successful"
        return response["data"]["token"]

    @classmethod
    @ttl_cache(TTL)
    def request_profile(cls, token) -> dict:
        response = loads(post(
            "https://sm.ms/api/v2/profile",
            headers={"Authorization": token}
        ).content)
        assert all((
            response["success"],
            response["code"] == "success",
            response["message"] == "Get user profile success."
        ))
        return response["data"]

    @classmethod
    def from_token(cls, token) -> "User":
        user = cls()
        user.token = token
        return user

    @classmethod
    def from_login(cls, username, password) -> "User":
        user = cls()
        user.username = username
        user.password = password
        return user

    def attempt(self, username="", password=""):
        self.token = self.request_token(username or self.username, password or self.password)

    @cached_property
    def username(self) -> str:
        return input("username/email: ")

    @cached_property
    def password(self) -> str:
        from getpass import getpass
        return getpass("password: ")

    @cached_property
    def token(self) -> str:
        return self.request_token(self.username, self.password)

    @property
    def profile(self) -> dict:
        return self.request_profile(self.token)

    @property
    def disk_usage(self) -> str:
        return self.profile["disk_usage"]

    @property
    def disk_limit(self) -> str:
        return self.profile["disk_limit"]

    @property
    def disk_usage_raw(self):
        return self.profile["disk_usage_raw"]

    @property
    def disk_limit_raw(self):
        return self.profile["disk_limit_raw"]
