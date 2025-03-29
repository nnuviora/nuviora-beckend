import uuid
import json
from abc import ABC, abstractmethod

from redis import Redis

from config import config_setting


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
        self.redis = Redis(
            host=config_setting.REDIS_HOST,
            port=config_setting.REDIS_PORT,
        )

    async def set(self, data: dict) -> str:
        try:
            token = str(uuid.uuid4())
            self.redis.set(token, json.dumps(data))
            self.redis.expire(token, 180)
            return token
        except Exception as e:
            raise Exception(f"Redis Set Error in {self.set.__name__}: {e}")

    async def get(self, token: str) -> dict:
        try:
            data = json.loads(self.redis.get(token)) or None
            return data
        except Exception as e:
            raise Exception(f"Redis Get Error in {self.get.__name__}: {e}")
