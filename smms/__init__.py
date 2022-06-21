__version__ = "0.1.2"

from .user import BaseUser
from .image import *


class User(BaseUser):
    def upload_image(self, filename, file=None):
        return upload_image(self.token, filename, file)

    # noinspection PyShadowingBuiltins
    def delete_image(self, hash):
        return delete_image(self.token, hash)

    def get_upload_history(self, page):
        return get_upload_history(self.token, page)

    def get_temp_upload_history(self):
        return get_temp_upload_history(self.token)

    def clear_temp_upload_history(self):
        return clear_temp_upload_history(self.token)


__all__ = ["User"]
