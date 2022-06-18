from requests import post
from orjson import loads
from functools import cached_property
from cachetools.func import ttl_cache


# noinspection PyPropertyAccess, PyAttributeOutsideInit
class User:
    def request_token(self, username="", password="") -> str:
        response = loads(post(
            "https://sm.ms/api/v2/token",
            {"username": username or self.username,
             "password": password or self.password}
        ).content)
        assert all((
            response["success"],
            response["code"] == "success",
            response["message"] == "Get API token success."
        )), "not successful"
        return response["data"]["token"]

    def request_profile(self, token="") -> dict:
        response = loads(post(
            "https://sm.ms/api/v2/profile",
            headers={"Authorization": token or self.token}
        ).content)
        assert all((
            response["success"],
            response["code"] == "success",
            response["message"] == "Get user profile success."
        ))
        return response["data"]

    def attempt(self, username="", password=""):
        self.token = self.request_token(username or self.username, password or self.password)

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

    @cached_property
    def username(self) -> str:
        return input("username/email: ")

    @cached_property
    def password(self) -> str:
        from getpass import getpass
        return getpass("password: ")

    @cached_property
    def token(self) -> str:
        return self.request_token()

    @cached_property
    def profile(self) -> dict:
        return self.request_profile()
