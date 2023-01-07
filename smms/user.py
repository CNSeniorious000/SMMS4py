from httpx import Client, AsyncClient
from .base import *


class User(BaseUser):
    def get_http_client(self) -> Client:
        return Client(
            http2=True,
            base_url="https://smms.app/api/v2/",
            headers={"Authorization": f"Basic {self.token}"}
        )

    def get_profile(self) -> UserProfile:
        res = loads(self.http_client.post("/profile").content)
        try:
            return UserProfile(**res["data"])
        except KeyError as err:
            raise ValueError(res) from err

    def get_upload_history(self, page: int) -> list[UploadHistoryItem]:
        res = loads(self.http_client.get(f"/upload_history?{page=}").content)
        try:
            return [UploadHistoryItem(**item) for item in res["data"]]
        except KeyError as err:
            raise ValueError(res) from err

    def get_upload_history_all(self) -> list[UploadHistoryItem]:
        results = result = self.get_upload_history(0)
        page = 0
        while len(result) == 100:
            page += 1
            result = self.get_upload_history(page)
            results.extend(result)

        return results

    def upload(self, filename: str, file, media_type: str) -> ImageUploaded:
        res = loads(self.http_client.post("/upload", files={"smfile": (filename, file, media_type)}).content)
        try:
            return ImageUploaded(**res["data"])
        except KeyError as err:
            raise ValueError(res) from err

    def delete(self, hash: str):
        return loads(self.http_client.get(f"/delete/{hash}").content)


class AsyncUser(BaseUser):
    def get_http_client(self) -> AsyncClient:
        return AsyncClient(
            http2=True,
            base_url="https://smms.app/api/v2/",
            headers={"Authorization": f"Basic {self.token}"}
        )

    async def get_profile(self) -> UserProfile:
        res = loads((await self.http_client.post("/profile")).content)
        try:
            return UserProfile(**res["data"])
        except KeyError as err:
            raise ValueError(res) from err

    http_client: AsyncClient

    async def get_upload_history(self, page: int) -> list[UploadHistoryItem]:
        res = loads((await self.http_client.get(f"/upload_history?{page=}")).content)
        try:
            return [UploadHistoryItem(**item) for item in res["data"]]
        except KeyError as err:
            raise ValueError(res) from err

    async def get_upload_history_all(self) -> list[UploadHistoryItem]:
        results = result = await self.get_upload_history(0)
        page = 0
        while len(result) == 100:
            page += 1
            result = await self.get_upload_history(page)
            results.extend(result)

        return results

    async def upload(self, filename: str, file, media_type: str) -> ImageUploaded:
        res = loads((await self.http_client.post("/upload", files={"smfile": (filename, file, media_type)})).content)
        try:
            return ImageUploaded(**res["data"])
        except KeyError as err:
            raise ValueError(res) from err

    async def delete(self, hash: str):
        return loads((await self.http_client.get(f"/delete/{hash}")).content)
