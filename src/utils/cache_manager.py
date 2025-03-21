import uuid
import json
from abc import ABC, abstractmethod

from redis import Redis


class AbstractCache(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    async def set(self, data: dict) -> str:
        pass

    @abstractmethod
    async def get(self, token: str) -> dict:
        pass


class RedisManager(AbstractCache):
    def __init__(self) -> None:
        self.redis = Redis(host=None, port=None)

    async def set(self, data: dict) -> str:
        token = uuid.uuid4()
        self.redis.hset(key=token, mapping=data)
        return token

    async def get(self, token: str) -> dict:
        data = self.redis.hget(key=token)
        return data
