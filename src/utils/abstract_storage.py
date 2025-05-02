from abc import ABC, abstractmethod


class AbstractStorage(ABC):
    @abstractmethod
    def upload_avatar(self, file_bytes: bytes, filename: str, content_type: str) -> str:
        """
        Upload avatar image and return its public URL.
        """
        pass
